from . import serializers, models
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from helper import keys, messages


class ProductListView(generics.ListAPIView):
    serializer_class = serializers.ProductSerializer
    model = serializer_class.Meta.model
    queryset = model.objects.all()
    permission_classes = [AllowAny]


class OrderListView(generics.ListCreateAPIView):
    serializer_class = serializers.OrderDataSerializer
    model = serializer_class.Meta.model
    queryset = model.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


class AddToCartView(generics.CreateAPIView):
    serializer_class = serializers.CartDataSerializer
    model = serializer_class.Meta.model
    queryset = model.objects.all()
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        product_id = request.data[keys.PRODUCT_ID]
        user = self.request.user
        user_cart_instance, created = self.model.objects.get_or_create(user=user)
        try:
            product_instance = models.ProductData.objects.get(id=product_id)
        except models.ProductData.DoesNotExist as e:
            print(e)
            return Response({keys.DETAIL: messages.PRODUCT_NOT_FOUND}, status=status.HTTP_400_BAD_REQUEST)
        if product_instance in user_cart_instance.product.all():
            return Response({keys.DETAIL: messages.ITEM_ALREADY_IN_CART}, status=status.HTTP_400_BAD_REQUEST)
        else:
            user_cart_instance.product.add(product_instance)
            return Response({keys.MESSAGE: messages.PRODUCT_ADDED_TO_CART}, status=status.HTTP_200_OK)


class CartView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.CartDataSerializer
    model = serializer_class.Meta.model
    queryset = model.objects.all()
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        user = self.request.user
        user_cart_instance, created = self.model.objects.get_or_create(user=user)
        serializer = serializers.CartDataSerializer(user_cart_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        product_id = request.data.get(keys.PRODUCT_ID, None)

        user = self.request.user
        user_cart_instance, created = self.model.objects.get_or_create(user=user)
        try:
            product_instance = models.ProductData.objects.get(id=product_id)
            user_cart_instance.product.remove(product_instance)
        except models.ProductData.DoesNotExist as e:
            print(e)
            return Response({keys.DETAIL: messages.PRODUCT_NOT_FOUND}, status=status.HTTP_400_BAD_REQUEST)

        serializer = serializers.CartDataSerializer(user_cart_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PlaceOrderView(generics.CreateAPIView):
    serializer_class = serializers.OrderDataSerializer
    model = serializer_class.Meta.model
    queryset = model.objects.all()
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        products = request.data.get(keys.PRODUCTS, [])
        amount = request.data.get(keys.AMOUNT, 0)
        user = self.request.user
        user_order_instance, created = self.model.objects.get_or_create(user=user, amount=amount)
        product_list = models.ProductData.objects.filter(id__in=products)
        user_order_instance.product.add(*product_list)
        user_cart_instance = models.CartData.objects.get(user=user)
        user_cart_instance.product.clear()
        return Response({keys.MESSAGE: messages.PRODUCT_ADDED_TO_CART}, status=status.HTTP_200_OK)

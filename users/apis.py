from . import serializers, models
from helper import messages, keys, methods
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import Token


class RegisterView(generics.CreateAPIView):
    serializer_class = serializers.UserSerializer
    model = serializer_class.Meta.model
    queryset = model.objects.all()

    def create(self, request, *args, **kwargs):
        email = request.data.get(keys.EMAIL, None)
        if models.UserData.objects.filter(email=email).exists():
            return Response({keys.DETAIL: messages.USER_WITH_EMAIL_ALREADY_EXISTS}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(data=request.data)
        print(serializer)

        if serializer.is_valid():
            print('true')
            user = serializer.save()
            print(user, user.email)
            token = methods.get_tokens_for_user(user)
            return Response({keys.MESSAGE: messages.USER_REGISTRATION_SUCCESFULL, keys.TOKEN: token},
                            status=status.HTTP_200_OK)
        return Response({keys.MESSAGE: serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

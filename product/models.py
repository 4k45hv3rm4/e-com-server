from django.db import models
from users import models as user_model


def upload_location(instance, filename, *args, **kwargs):
    file_path = 'ecom/{filename}'.format(filename=filename
                                   )
    return file_path


class ProductData(models.Model):
    title = models.CharField(max_length=255)
    image = models.FileField(upload_to=upload_location, null=True, blank=True)
    description = models.TextField()
    price = models.FloatField()

    def __str__(self):
        return self.title


class OrderData(models.Model):
    product = models.ManyToManyField(to=ProductData)
    amount = models.FloatField()
    user = models.ForeignKey(to=user_model.UserData, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.__str__()


class CartData(models.Model):
    product = models.ManyToManyField(ProductData, related_name='products')
    user = models.OneToOneField(user_model.UserData, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.__str__()
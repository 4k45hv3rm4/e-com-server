from product import utils, models
from django.core.management import BaseCommand


class Command(BaseCommand):
    help = 'Fetch Upcoming Matches from entity sports API'

    def handle(self, *args, **kwargs):
        product_list = utils.product_data
        for item in product_list:
            models.ProductData.objects.create(title=item['title'], price=item['price'], description=item['description'])

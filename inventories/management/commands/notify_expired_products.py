from datetime import date, timedelta

from django.core.management.base import BaseCommand

from accounts.models import User
from inventories.models import Product


class Command(BaseCommand):
    help = 'Notify expired products'

    def handle(self, *args, **options):
        users = User.objects.all()

        for user in users:
            default_date = date.today() + timedelta(days=3)
            products = user.products.filter(
                expiration_date__lte=default_date).order_by('expiration_date')

            print('{} : {} produits périment aujourd\'hui'.format(user.email, len(products)))

            if len(products):
                context = {
                    'count': len(products),
                    'products': products
                }

                user.send_user_email(
                    subject_tmpl='products_expiration_notification/subject.txt',
                    body_txt_tmpl='products_expiration_notification/body.txt',
                    body_html_tmpl='products_expiration_notification/body.html',
                    context=context,
                )

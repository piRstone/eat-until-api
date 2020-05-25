from datetime import date

from django.core.management.base import BaseCommand

from accounts.models import User


class Command(BaseCommand):
    help = 'Notify expired products'

    def handle(self, *args, **options):
        users = User.objects.all()

        for user in users:
            default_date = date.today()
            products = user.products.filter(
                notification_date=default_date).order_by('expiration_date')

            print('{} : {} produits périment aujourd\'hui'.format(user.email, len(products)))

            if products:
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

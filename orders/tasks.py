from Django_shop.celery import app
from .service import send
from orders.models import Order
from django.core.mail import send_mail


@app.task
def send_spam_email(user_email):
    send(user_email)


# @app.task
# def send_much_letters():
#     for order in Order.objects.all():
#         send_mail(
#             'Вы подписались на рассылку',
#             'fwpefpwkfpowkepfk',
#             'nik.vagin1995@gmail.com',
#             [order.email],
#             fail_silently=False
#         )

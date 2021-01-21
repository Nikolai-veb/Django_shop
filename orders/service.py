from django.core.mail import send_mail


def send(hand, body,user_email):
    send_mail(
        hand,
        body,
        'nik.vagin1995@gmail.com',
        [user_email],
        fail_silently=False,

    )

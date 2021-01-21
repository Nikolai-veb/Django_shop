from django.core.mail import send_mail


def send(title, body, user_email):
    send_mail(
        title,
        body,
        'nik.vagin1995@gmail.com',
        [user_email],
        fail_silently=False,

    )

from django.conf import settings
from django.utils import timezone

from apscheduler.schedulers.background import BackgroundScheduler
from django.core.mail import send_mail
from config.settings import EMAIL_HOST_USER
from mailing.models import NewsLetter, SendingAttempt


def send_mailing(mailing):
    emails_list = mailing.client.filter(status='active').values_list('email', flat='True')

    try:
        send_mail(
            subject=mailing.message.subject,
            message=mailing.message.body_letter,
            from_email=EMAIL_HOST_USER,
            recipient_list=list(emails_list)
        )
    except Exception as e:
        SendingAttempt.objects.create(mailing=mailing, error=e, status='fail', response='Сообщение не доставлено')
    else:
        SendingAttempt.objects.create(mailing=mailing, status='success', response='Сообщение доставлено')


# Функция для запуска планировщика
def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(send_scheduled_mailings, 'interval', hours=1)  # Запланировать выполнение раз в час
    scheduler.start()


# Функция для отправки запланированных рассылок
def send_scheduled_mailings():
    current_time = timezone.now()  # Получаем текущее время
    mailings = NewsLetter.objects.filter(first_time_sending=current_time, status='active')  # Получаем активные рассылки
    for mailing in mailings:
        send_mailing(mailing)  # Отправляем рассылку

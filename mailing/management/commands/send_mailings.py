from django.core.management.base import BaseCommand
from mailing.tasks import send_scheduled_mailings


class Command(BaseCommand):
    help = 'Send mailings'  # Описание команды

    def handle(self, *args, **options):
        send_scheduled_mailings()  # Вызываем функцию для отправки рассылок

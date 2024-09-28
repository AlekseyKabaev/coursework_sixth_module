from django.db import models

from users.models import User

NULLABLE = {'null': True, 'blank': True}  # Параметры для указания, что поля могут быть пустыми


class Client(models.Model):
    """Модель для клиентов"""
    email = models.EmailField(unique=True, verbose_name='email')
    first_name = models.CharField(max_length=50, verbose_name='Имя')
    last_name = models.CharField(max_length=50, verbose_name='Фамилия')
    patronymic = models.CharField(max_length=50, verbose_name='Отчество', **NULLABLE)
    comment = models.TextField(verbose_name='Комментарий', **NULLABLE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='clients', verbose_name='Владелец',
                              **NULLABLE)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"
        ordering = ("email",)
        permissions = [
            ("can_edit_is_active_client", "Can edit active clients"),
        ]

    def __str__(self):
        return self.email


class Message(models.Model):
    """Модель для сообщений"""
    subject = models.CharField(max_length=100, verbose_name='Тема письма')
    body_letter = models.TextField(verbose_name='Тело письма')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages', verbose_name='Владелец',
                              **NULLABLE)

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"
        ordering = ("subject",)

    def __str__(self):
        return self.subject


class NewsLetter(models.Model):
    """Модель для рассылок"""
    # Возможные варианты периодичности рассылок
    PERIOD_CHOICES = [
        ('daily', 'Раз в день'),
        ('weekly', 'Раз в неделю'),
        ('monthly', 'Раз в месяц'),
    ]

    # Возможные статусы рассылок
    STATUS_CHOICES = [
        ('active', 'Активная'),
        ('inactive', 'Неактивная'),
    ]

    first_time_sending = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время первой отправки рассылки')
    frequency = models.CharField(max_length=10, choices=PERIOD_CHOICES, verbose_name='Переодичность')
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, verbose_name='Статус рассылки')
    # Связь с сообщением (один к одному)
    message = models.OneToOneField(Message, on_delete=models.CASCADE, related_name='newsletter',
                                   verbose_name='Сообщение')
    # Связь с клиентами (многие к одному)
    clients = models.ManyToManyField(Client, related_name='newsletters', verbose_name='Клиенты')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='newsletters', verbose_name='Владелец',
                              **NULLABLE)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"
        ordering = ("status",)
        permissions = [
            ("can_edit_is_active_mailing", "Can edit active newsletters"),
        ]

    def __str__(self):
        return self.status


class SendingAttempt(models.Model):
    """Модель для попыток отправки рассылок"""
    newsletter = models.ForeignKey(NewsLetter, on_delete=models.CASCADE, related_name='sending_attempts',
                                   verbose_name='Рассылка')
    last_attempt_time = models.DateTimeField(auto_now=True, verbose_name='Дата и время последней рассылки')
    status = models.BooleanField(default=False, verbose_name='Статус попытки')
    server_response = models.TextField(verbose_name='Ответ почтового сервера, если он был', **NULLABLE)

    class Meta:
        verbose_name = "Попытка рассылки"
        verbose_name_plural = "Попытка рассылок"
        ordering = ("status",)

    def __str__(self):
        return f'Попытка рассылки: {"успешно" if self.status else "не успешно"}'

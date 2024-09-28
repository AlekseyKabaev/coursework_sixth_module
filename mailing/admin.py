from django.contrib import admin
from mailing.models import NewsLetter, Client, Message, SendingAttempt


@admin.register(NewsLetter)
class NewsLetterAdmin(admin.ModelAdmin):
    list_display = ['status', 'message', 'frequency', 'first_time_sending']
    list_filter = ('status',)
    search_fields = ('status', 'message', 'clients')


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'patronymic', 'email', 'comment']
    list_filter = ('email',)
    search_fields = ('first_name', 'last_name', 'patronymic')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['subject', 'body_letter']
    list_filter = ('subject',)
    search_fields = ('subject', 'body_letter')


@admin.register(SendingAttempt)
class SendingAttemptAdmin(admin.ModelAdmin):
    list_display = ['status', 'last_attempt_time', 'newsletter', 'server_response']
    list_filter = ('status',)
    search_fields = ('status', 'last_attempt_time', 'newsletter')

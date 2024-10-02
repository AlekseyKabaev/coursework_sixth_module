from django.urls import path
from django.views.decorators.cache import cache_page

from mailing.apps import MailingConfig
from mailing.views import NewsLetterCreateView, NewsLetterListView, NewsLetterDetailView, NewsLetterUpdateView, \
    NewsLetterDeleteView, ClientCreateView, ClientListView, ClientDetailView, ClientUpdateView, ClientDeleteView, \
    MessageCreateView, MessageListView, MessageDetailView, MessageUpdateView, MessageDeleteView, HomePageView, \
    disabling_client, disabling_newsletter, SendingAttemptListView

app_name = MailingConfig.name

urlpatterns = [
    path("", HomePageView.as_view(), name="base"),
    path('newsletter_create/', NewsLetterCreateView.as_view(), name='newsletter_create'),
    path('newsletter_list/', NewsLetterListView.as_view(), name='newsletter_list'),
    path('newsletter/<int:pk>/', cache_page(60)(NewsLetterDetailView.as_view()), name='newsletter_detail'),
    path('newsletter/<int:pk>/update/', NewsLetterUpdateView.as_view(), name='newsletter_update'),
    path('newsletter/<int:pk>/delete/', NewsLetterDeleteView.as_view(), name='newsletter_delete'),

    path('client_create/', ClientCreateView.as_view(), name='client_create'),
    path('client_list/', ClientListView.as_view(), name='client_list'),
    path('client/<int:pk>/', cache_page(60)(ClientDetailView.as_view()), name='client_detail'),
    path('client/<int:pk>/update/', ClientUpdateView.as_view(), name='client_update'),
    path('client/<int:pk>/delete/', ClientDeleteView.as_view(), name='client_delete'),

    path('message_create/', MessageCreateView.as_view(), name='message_create'),
    path('message_list/', MessageListView.as_view(), name='message_list'),
    path('message/<int:pk>/', cache_page(60)(MessageDetailView.as_view()), name='message_detail'),
    path('message/<int:pk>/update/', MessageUpdateView.as_view(), name='message_update'),
    path('message/<int:pk>/delete/', MessageDeleteView.as_view(), name='message_delete'),

    path("activity/<int:pk>/client/", disabling_client, name="disabling_client"),
    path("activity/<int:pk>/newsletter/", disabling_newsletter, name="disabling_newsletter"),

    path('sendingattempt_list/', SendingAttemptListView.as_view(), name='sending_list'),

]

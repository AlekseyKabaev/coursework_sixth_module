import random

from django.core.exceptions import PermissionDenied

from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from mailing.models import NewsLetter, Client, Message, SendingAttempt
from mailing.forms import NewsLetterForm, ClientForm, MessageForm, NewsLetterManagerForm
from blog.models import Blog


class HomePageView(TemplateView):
    template_name = "mailing/base.html"

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data['newsletter_list'] = NewsLetter.objects.count()
        context_data['newsletter_list_active'] = NewsLetter.objects.filter(is_active=True).count()
        context_data['client_list'] = Client.objects.count()
        blog_posts = list(Blog.objects.all())
        context_data['blog_list'] = random.sample(blog_posts, min(3, len(blog_posts)))
        context_data['is_base'] = True

        return context_data


class NewsLetterCreateView(LoginRequiredMixin, CreateView):
    model = NewsLetter
    form_class = NewsLetterForm
    success_url = reverse_lazy('mailing:newsletter_list')

    def form_valid(self, form):
        newsletter = form.save()
        user = self.request.user
        newsletter.owner = user
        newsletter.save()
        return super().form_valid(form)


class NewsLetterListView(LoginRequiredMixin, ListView):
    model = NewsLetter

    def get_queryset(self):
        return NewsLetter.objects.filter(owner=self.request.user)

    def get_form_class(self):
        user = self.request.user
        if user == self.object.owner:
            return NewsLetterForm
        elif (user.has_perm("mailing.view_newsletter") and
              user.has_perm("can_edit_is_active_mailing")):
            return NewsLetterManagerForm
        raise PermissionDenied


class NewsLetterDetailView(LoginRequiredMixin, DetailView):
    model = NewsLetter


class NewsLetterUpdateView(LoginRequiredMixin, UpdateView):
    model = NewsLetter
    form_class = NewsLetterForm
    success_url = reverse_lazy('mailing:newsletter_list')


class NewsLetterDeleteView(LoginRequiredMixin, DeleteView):
    model = NewsLetter
    success_url = reverse_lazy('mailing:newsletter_list')


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailing:client_list')

    def form_valid(self, form):
        client = form.save()
        user = self.request.user
        client.owner = user
        client.save()
        return super().form_valid(form)


class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    permission_required = 'mailing.view_client'

    def get_queryset(self):
        return Client.objects.filter(owner=self.request.user)

    def get_form_class(self):
        user = self.request.user
        if user == self.object.owner:
            return NewsLetterForm
        elif (user.has_perm("mailing.view_newsletter") and
              user.has_perm("can_edit_is_active_mailing")):
            return NewsLetterManagerForm
        raise PermissionDenied


class ClientDetailView(LoginRequiredMixin, DetailView):
    model = Client


class ClientUpdateView(LoginRequiredMixin, UpdateView, ):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailing:client_list')


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = Client
    success_url = reverse_lazy('mailing:client_list')


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('mailing:message_list')

    def form_valid(self, form):
        message = form.save()
        user = self.request.user
        message.owner = user
        message.save()
        return super().form_valid(form)


class MessageListView(LoginRequiredMixin, ListView):
    model = Message

    def get_queryset(self):
        return Message.objects.filter(owner=self.request.user)


class MessageDetailView(LoginRequiredMixin, DetailView):
    model = Message


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('mailing:message_list')


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    success_url = reverse_lazy('mailing:message_list')


def disabling_client(request, pk):
    client_item = get_object_or_404(Client, pk=pk, owner=request.user)
    if client_item.is_active:
        client_item.is_active = False
    else:
        client_item.is_active = True

    client_item.save()

    return redirect(reverse('mailing:client_list'))


def disabling_newsletter(request, pk):
    newsletter_item = get_object_or_404(NewsLetter, pk=pk, owner=request.user)
    if newsletter_item.is_active:
        newsletter_item.is_active = False
    else:
        newsletter_item.is_active = True

    newsletter_item.save()

    return redirect(reverse('mailing:newsletter_list'))


class SendingAttemptListView(LoginRequiredMixin, ListView):
    model = SendingAttempt

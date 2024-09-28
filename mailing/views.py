import random

from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from mailing.models import NewsLetter, Client, Message
from mailing.forms import NewsLetterForm, ClientForm, MessageForm
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


class NewsLetterCreateView(CreateView, LoginRequiredMixin, PermissionRequiredMixin):
    model = NewsLetter
    form_class = NewsLetterForm
    success_url = reverse_lazy('mailing:newsletter_list')

    def form_valid(self, form):
        newsletter = form.save()
        user = self.request.user
        newsletter.owner = user
        newsletter.save()
        return super().form_valid(form)


class NewsLetterListView(ListView, LoginRequiredMixin):
    model = NewsLetter


class NewsLetterDetailView(DetailView, LoginRequiredMixin):
    model = NewsLetter


class NewsLetterUpdateView(UpdateView, LoginRequiredMixin, PermissionRequiredMixin):
    model = NewsLetter
    form_class = NewsLetterForm
    success_url = reverse_lazy('mailing:newsletter_list')


class NewsLetterDeleteView(DeleteView, LoginRequiredMixin, PermissionRequiredMixin):
    model = NewsLetter
    success_url = reverse_lazy('mailing:newsletter_list')


class ClientCreateView(CreateView, LoginRequiredMixin, PermissionRequiredMixin):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailing:client_list')

    def form_valid(self, form):
        client = form.save()
        user = self.request.user
        client.owner = user
        client.save()
        return super().form_valid(form)


class ClientListView(ListView, LoginRequiredMixin):
    model = Client


class ClientDetailView(DetailView, LoginRequiredMixin):
    model = Client


class ClientUpdateView(UpdateView, LoginRequiredMixin, PermissionRequiredMixin):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailing:client_list')


class ClientDeleteView(DeleteView, LoginRequiredMixin, PermissionRequiredMixin):
    model = Client
    success_url = reverse_lazy('mailing:client_list')


class MessageCreateView(CreateView, LoginRequiredMixin, PermissionRequiredMixin):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('mailing:message_list')

    def form_valid(self, form):
        message = form.save()
        user = self.request.user
        message.owner = user
        message.save()
        return super().form_valid(form)


class MessageListView(ListView, LoginRequiredMixin):
    model = Message


class MessageDetailView(DetailView, LoginRequiredMixin):
    model = Message


class MessageUpdateView(UpdateView, LoginRequiredMixin, PermissionRequiredMixin):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('mailing:message_list')


class MessageDeleteView(DeleteView, LoginRequiredMixin, PermissionRequiredMixin):
    model = Message
    success_url = reverse_lazy('mailing:message_list')


def disabling_client(request, pk):
    client_item = get_object_or_404(Client, pk=pk)
    if client_item.is_active:
        client_item.is_active = False
    else:
        client_item.is_active = True

    client_item.save()

    return redirect(reverse('mailing:client_list'))


def disabling_newsletter(request, pk):
    client_item = get_object_or_404(NewsLetter, pk=pk)
    if client_item.is_active:
        client_item.is_active = False
    else:
        client_item.is_active = True

    client_item.save()

    return redirect(reverse('mailing:newsletter_list'))
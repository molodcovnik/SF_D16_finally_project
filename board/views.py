from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.db.models import Count
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import (ListView, DetailView, CreateView, UpdateView, DeleteView)
from django.views.generic.edit import FormMixin
from django.http import Http404, HttpResponseForbidden

from accounts.models import Profile
from .models import Item, Category, Reply, ItemCategory
from .forms import ItemForm, ReplyForm
from .filters import ItemFilter, ReplyFilter
from accounts.signals import random_code


# Create your views here.
class HomePageView(ListView):
    model = Reply
    template_name = 'home_page.html'
    context_object_name = 'replies'

    def get_queryset(self):
        queryset = Reply.objects.all().values(
            'item__id', 'item__description', 'item__header', 'item__date', 'item__category', 'item__image').annotate(
            total=Count('item_id')).order_by('-total')[:3]
        return queryset


class ItemList(ListView):
    model = Item
    ordering = '-date'
    template_name = 'items.html'
    context_object_name = 'items'
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = ItemFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class ItemDetail(DetailView, FormMixin, LoginRequiredMixin):
    model = Item
    template_name = 'item.html'
    context_object_name = 'item'
    form_class = ReplyForm

    def get_success_url(self, **kwargs):
        return reverse_lazy('item_detail', kwargs={'pk': self.get_object().id})

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.item = self.get_object()
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            self.user = self.request.user
            item = Item.objects.get(id=self.kwargs['pk'])
            context['count'] = Reply.objects.filter(item=item).count()
            context['count_user'] = Reply.objects.filter(item=item, user=self.user).count()
            context['replies'] = Reply.objects.filter(item=item)
            context['reply_user'] = Reply.objects.filter(item=item, user=self.user)
        except:
            raise PermissionDenied
        return context


class ItemCreate(CreateView, FormMixin, LoginRequiredMixin):
    #raise_exception = True
    form_class = ItemForm
    model = Item
    template_name = 'item_create.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        try:
            self.object.user = self.request.user

            if self.object.user.profile.is_confirmed:
                self.object.save()
                return super().form_valid(form)
            else:
                raise PermissionDenied
        except:
            raise PermissionDenied


class ItemDetailNonAccess(DetailView):
    model = Item
    template_name = 'item_non_access.html'
    context_object_name = 'item'
    form_class = ReplyForm

    def get_success_url(self, **kwargs):
        return reverse_lazy('item_detail', kwargs={'pk': self.get_object().id})


class ItemEdit(UpdateView, LoginRequiredMixin):
    raise_exception = True
    form_class = ItemForm
    model = Item
    template_name = 'item_edit.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.request.user != kwargs['instance'].user:
            return self.handle_no_permission()
        return kwargs


class ItemDelete(DeleteView, LoginRequiredMixin):
    model = Item
    template_name = 'item_delete.html'
    success_url = reverse_lazy('item_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.request.user != self.object.user:
            return self.handle_no_permission()
        return kwargs


class ReplyCreate(CreateView, LoginRequiredMixin):
    raise_exception = True
    form_class = ReplyForm
    model = Reply
    template_name = 'reply_create.html'
    success_url = reverse_lazy('item_list')


class ReplyEdit(UpdateView, LoginRequiredMixin):
    form_class = ReplyForm
    model = Reply
    template_name = 'reply_create.html'

    def get_success_url(self, **kwargs):
        return reverse_lazy('item_detail', kwargs={'pk': self.get_object().item.id})


class ReplyList(ListView, LoginRequiredMixin):
    model = Reply
    template_name = 'reply_list.html'
    ordering = '-date'
    context_object_name = 'replies'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.user = self.request.user
        self.filterset = ReplyFilter(self.request.GET, queryset=Reply.objects.filter(item__user=self.user).order_by('-date'))
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.user = self.request.user
        context['filterset'] = self.filterset
        context['replies_accepted'] = Reply.objects.filter(item__user=self.user, accepted=True)
        return context


@login_required
def accept_reply(request, pk):
    reply = Reply.objects.get(id=pk)
    reply.accepted = True
    reply.save()
    return HttpResponseRedirect(reverse_lazy('reply_list'))

@login_required
def reject_reply(request, pk):
    reply = Reply.objects.get(id=pk)
    reply.accepted = False
    reply.save()
    return HttpResponseRedirect(reverse_lazy('reply_list'))

@login_required
def delete_reply(request, pk):
    reply = Reply.objects.get(id=pk)
    reply.delete()
    return HttpResponseRedirect(reverse_lazy('reply_list'))


class MySalesList(ListView, LoginRequiredMixin):
    model = Item
    template_name = 'my_sales_list.html'
    context_object_name = 'items'
    paginate_by = 10

    def get_queryset(self):
        self.user = self.request.user
        queryset = Item.objects.filter(user=self.user).order_by('-date')
        return queryset


class MyPurchasesList(ListView, LoginRequiredMixin):
    model = Reply
    template_name = 'my_purchases_list.html'
    context_object_name = 'replies'
    paginate_by = 10

    def get_queryset(self):
        self.user = self.request.user
        queryset = Reply.objects.filter(user=self.user).order_by('-date')
        return queryset


@login_required
def mail_code(request):
    user = request.user
    code = random_code()
    Profile.objects.create(user=user, code=code)
    return HttpResponseRedirect(reverse_lazy('confirm_code'))


from django.shortcuts import render, get_object_or_404
from .forms import UserForm, UserUpdateForm, ChangePassForm
from django.views.generic import CreateView, TemplateView, ListView, UpdateView, DetailView, View
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from ecom.models import Order


@login_required
def user_order(request):
    u_orders = Order.objects.filter(user=request.user, order_status=True)
    return render(request, 'accounts/order_list.html', {'u_orders': u_orders})


@login_required()
def user_order_details(request, pk):
    order_details = Order.objects.get(user=request.user, pk=pk)
    print(order_details)
    return render(request, 'accounts/order_details.html', {'order_details': order_details})


class SignUp(CreateView):
    form_class = UserForm
    success_url = reverse_lazy('accounts:login')
    template_name = 'accounts/signup.html'


class ProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'accounts/user_detail.html'


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'accounts/user_form.html'
    success_url = reverse_lazy('accounts:profile_view')


class ChangePass(LoginRequiredMixin, PasswordChangeView):
    model = User
    form_class = ChangePassForm
    template_name = 'accounts/change_password_form.html'
    success_url = reverse_lazy('accounts:home')
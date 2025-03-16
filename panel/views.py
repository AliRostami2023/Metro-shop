from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView, ListView
from account.models import User
from order.models import Order
from panel.forms import ChangePasswordUserForm, EditProfileModelForm



class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'panel/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['user'] = User.objects.filter(id=self.request.user.id).first()
        return context


def sidebar_profile_component(request):
    user = User.objects.filter(id=request.user.id).first()
    return render(request, 'panel/components/sidebar-profile-component.html', {'user': user})


class EditInfoUserView(LoginRequiredMixin, View):
    template_name = 'panel/edit-info.html'
    form_class = EditProfileModelForm

    def setup(self, request, *args, **kwargs):
        self.user_instance = User.objects.filter(id=request.user.id).first()
        return super().setup(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class(instance=self.user_instance)
        return render(request, self.template_name, {'form': form, 'current_user': self.user_instance})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES, instance=self.user_instance)

        if form.is_valid():
            form.save()
            return redirect(reverse('profile-page'))
        return render(request, self.template_name, {'form': form, 'current_user': self.user_instance})


class ChangePasswordPanel(LoginRequiredMixin, View):
    template_name = 'panel/change-password.html'
    form_class = ChangePasswordUserForm

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            current_user: User = User.objects.filter(id=request.user.id).first()
            if current_user.check_password(form.cleaned_data.get('current_password')):
                current_user.set_password(form.cleaned_data.get('new_password'))
                current_user.save()
                logout(request)
                return redirect(reverse('login-page'))
            else:
                form.add_error('current_password', 'current password is wrong!!!')
        return render(request, self.template_name, {'form': form})


class MyShopping(LoginRequiredMixin, ListView):
    template_name = 'panel/orders.html'
    model = Order
    context_object_name = 'orders'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(user_id=self.request.user.id, is_paid=True)
        return queryset


@login_required
def my_shopping_detail(request, order_id):
    order = Order.objects.prefetch_related('order_items').filter(id=order_id, user_id=request.user.id).first()

    if order is None:
        return Http404('this order is none')
    return render(request, 'panel/order-detail.html', {'order': order})

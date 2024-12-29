from django.shortcuts import render, redirect
from django.views.generic import TemplateView, CreateView
from .models import Group, Expense
from .forms import GroupForm, ExpenseForm
from django.urls import reverse_lazy

from django.utils import timezone


# Create your views here.

class BaseView(TemplateView):
    template_name = 'base/base.html'

class HomeView(TemplateView):
    template_name = 'base/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['groups'] = Group.objects.all()
        return context

class ModalTestView(TemplateView):
    template_name = 'modal/test.html'

class CreateGroupView(CreateView):
    template_name = 'modal/create_group_modal.html'
    form_class = GroupForm
    success_url = reverse_lazy('home')
    model = Group

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_group_form'] = GroupForm()
        return context


    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.save()
        form.instance.members.set(form.cleaned_data['members'])
        return super().form_valid(form)


class GroupDetailsView(TemplateView):
    template_name = 'details_page/group_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['group'] = Group.objects.get(id=kwargs['pk'])
        return context


class CreateExpenseView(CreateView):
    template_name = 'forms/create_expense.html'
    form_class = ExpenseForm
    success_url = reverse_lazy('home')
    model = Expense

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_expense_form'] = ExpenseForm()
        return context

    def form_valid(self, form):
        form.instance.added_by = self.request.user
        form.instance.last_updated_by = self.request.user
        form.instance.date = timezone.now()
        form.instance.save()
        form.instance.expenses.add(form.cleaned_data['group'])
        form.instance.included_users.set(form.cleaned_data['included_users'])
        form.instance.split_equally()
        return super().form_valid(form)


class ExpenseDetailsView(TemplateView):
    template_name = 'details_page/expense_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['expense'] = Expense.objects.get(id=kwargs['pk'])
        return context
    


class CreateExpenseModalView(CreateView):
    template_name = 'modal/create_expense_modal.html'
    form_class = ExpenseForm
    success_url = reverse_lazy('home')
    model = Expense
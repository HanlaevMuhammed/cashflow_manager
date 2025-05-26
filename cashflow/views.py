from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.http import JsonResponse

from .models import CashFlowRecord, Status, Type, Category, SubCategory
from .forms import (
    CashFlowRecordForm,
    CategoryForm,
    SubCategoryForm,
    TypeForm,
    StatusForm,
)


class CashFlowRecordListView(ListView):
    model = CashFlowRecord
    template_name = 'cashflow/record_list.html'
    context_object_name = 'records'
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset()
        date_from = self.request.GET.get('date_from')
        date_to = self.request.GET.get('date_to')
        status = self.request.GET.get('status')
        type_ = self.request.GET.get('type')
        category = self.request.GET.get('category')
        subcategory = self.request.GET.get('subcategory')

        if date_from:
            qs = qs.filter(date__gte=date_from)
        if date_to:
            qs = qs.filter(date__lte=date_to)
        if status:
            qs = qs.filter(status_id=status)
        if type_:
            qs = qs.filter(type_id=type_)
        if category:
            qs = qs.filter(category_id=category)
        if subcategory:
            qs = qs.filter(subcategory_id=subcategory)

        return qs.select_related('status', 'type', 'category', 'subcategory').order_by('-date', '-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['statuses'] = Status.objects.all()
        context['types'] = Type.objects.all()
        context['categories'] = Category.objects.all()
        context['subcategories'] = SubCategory.objects.all()
        context['filter_values'] = {
            'date_from': self.request.GET.get('date_from', ''),
            'date_to': self.request.GET.get('date_to', ''),
            'status': self.request.GET.get('status', ''),
            'type': self.request.GET.get('type', ''),
            'category': self.request.GET.get('category', ''),
            'subcategory': self.request.GET.get('subcategory', ''),
        }
        return context


class CashFlowRecordCreateView(CreateView):
    model = CashFlowRecord
    form_class = CashFlowRecordForm
    template_name = 'cashflow/record_form.html'
    success_url = reverse_lazy('cashflow:record_list')


class CashFlowRecordUpdateView(UpdateView):
    model = CashFlowRecord
    form_class = CashFlowRecordForm
    template_name = 'cashflow/record_form.html'
    success_url = reverse_lazy('cashflow:record_list')


class CashFlowRecordDeleteView(DeleteView):
    model = CashFlowRecord
    template_name = 'cashflow/record_confirm_delete.html'
    success_url = reverse_lazy('cashflow:record_list')


def load_categories(request):
    type_id = request.GET.get('type')
    categories = Category.objects.filter(type_id=type_id).order_by('name') if type_id else Category.objects.none()
    data = [{'id': cat.id, 'name': cat.name} for cat in categories]
    return JsonResponse(data, safe=False)


def load_subcategories(request):
    category_id = request.GET.get('category')
    subcategories = SubCategory.objects.filter(category_id=category_id).order_by('name') if category_id else SubCategory.objects.none()
    data = [{'id': sub.id, 'name': sub.name} for sub in subcategories]
    return JsonResponse(data, safe=False)


def manage_categories(request):
    if request.method == 'POST':
        if 'add_category' in request.POST:
            cat_form = CategoryForm(request.POST, prefix='cat')
            subcat_form = SubCategoryForm(prefix='subcat')
            type_form = TypeForm(prefix='type')
            if cat_form.is_valid():
                cat_form.save()
                return redirect('cashflow:manage_categories')
        elif 'add_subcategory' in request.POST:
            cat_form = CategoryForm(prefix='cat')
            subcat_form = SubCategoryForm(request.POST, prefix='subcat')
            type_form = TypeForm(prefix='type')
            if subcat_form.is_valid():
                subcat_form.save()
                return redirect('cashflow:manage_categories')
        elif 'add_type' in request.POST:
            cat_form = CategoryForm(prefix='cat')
            subcat_form = SubCategoryForm(prefix='subcat')
            type_form = TypeForm(request.POST, prefix='type')
            if type_form.is_valid():
                type_form.save()
                return redirect('cashflow:manage_categories')
        elif 'add_status' in request.POST:
            cat_form = CategoryForm(prefix='cat')
            subcat_form = SubCategoryForm(prefix='subcat')
            type_form = TypeForm(request.POST, prefix='type')
            status_form = StatusForm(request.POST, prefix='status')
            if status_form.is_valid():
                status_form.save()
                return redirect('cashflow:manage_categories')
    else:
        cat_form = CategoryForm(prefix='cat')
        subcat_form = SubCategoryForm(prefix='subcat')
        type_form = TypeForm(prefix='type')
        status_form = StatusForm(prefix='status')

    categories = Category.objects.all()
    subcategories = SubCategory.objects.select_related('category').all()
    types = Type.objects.all()
    statuses = Status.objects.all()

    context = {
        'cat_form': cat_form,
        'subcat_form': subcat_form,
        'type_form': type_form,
        'status_form': status_form,
        'categories': categories,
        'subcategories': subcategories,
        'types': types,
        'statuses': statuses,
    }
    return render(request, 'cashflow/manage_categories.html', context)


class CategoryUpdateView(UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'cashflow/category_form.html'
    success_url = reverse_lazy('cashflow:manage_categories')


class CategoryDeleteView(DeleteView):
    model = Category
    template_name = 'cashflow/category_confirm_delete.html'
    success_url = reverse_lazy('cashflow:manage_categories')


class SubCategoryUpdateView(UpdateView):
    model = SubCategory
    form_class = SubCategoryForm
    template_name = 'cashflow/subcategory_form.html'
    success_url = reverse_lazy('cashflow:manage_categories')


class SubCategoryDeleteView(DeleteView):
    model = SubCategory
    template_name = 'cashflow/subcategory_confirm_delete.html'
    success_url = reverse_lazy('cashflow:manage_categories')


class TypeUpdateView(UpdateView):
    model = Type
    form_class = TypeForm
    template_name = 'cashflow/type_form.html'
    success_url = reverse_lazy('cashflow:manage_categories')


class TypeDeleteView(DeleteView):
    model = Type
    template_name = 'cashflow/type_confirm_delete.html'
    success_url = reverse_lazy('cashflow:manage_categories')
    

class StatusUpdateView(UpdateView):
    model = Status
    form_class = StatusForm
    template_name = 'cashflow/status_form.html'
    success_url = reverse_lazy('cashflow:manage_categories')


class StatusDeleteView(DeleteView):
    model = Status
    template_name = 'cashflow/status_confirm_delete.html'
    success_url = reverse_lazy('cashflow:manage_categories')

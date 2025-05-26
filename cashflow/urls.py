from django.urls import path
from . import views

app_name = 'cashflow'

urlpatterns = [
    # Записи движения денежных средств
    path('', views.CashFlowRecordListView.as_view(), name='record_list'),
    path('create/', views.CashFlowRecordCreateView.as_view(), name='record_create'),
    path('edit/<int:pk>/', views.CashFlowRecordUpdateView.as_view(), name='record_edit'),
    path('delete/<int:pk>/', views.CashFlowRecordDeleteView.as_view(), name='record_delete'),

    path('manage_categories/', views.manage_categories, name='manage_categories'),

    # Редактирование категорий, подкатегорий, типов и статуса
    path('category/edit/<int:pk>/', views.CategoryUpdateView.as_view(), name='category_edit'),
    path('category/delete/<int:pk>/', views.CategoryDeleteView.as_view(), name='category_delete'),

    path('subcategory/edit/<int:pk>/', views.SubCategoryUpdateView.as_view(), name='subcategory_edit'),
    path('subcategory/delete/<int:pk>/', views.SubCategoryDeleteView.as_view(), name='subcategory_delete'),

    path('type/edit/<int:pk>/', views.TypeUpdateView.as_view(), name='type_edit'),
    path('type/delete/<int:pk>/', views.TypeDeleteView.as_view(), name='type_delete'),


path('status/edit/<int:pk>/', views.StatusUpdateView.as_view(), name='status_edit'),
path('status/delete/<int:pk>/', views.StatusDeleteView.as_view(), name='status_delete'),


    # AJAX пути для динамической загрузки категорий и подкатегорий
    path('ajax/load-categories/', views.load_categories, name='ajax_load_categories'),
    path('ajax/load-subcategories/', views.load_subcategories, name='ajax_load_subcategories'),
    
    
]

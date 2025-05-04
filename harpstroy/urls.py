from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('price/', views.PriceView.as_view(), name='price'),
    path('contacts/', views.ContactsView.as_view(), name='contacts'),
    path('submit-contact-form/', views.submit_contact_form, name='submit_contact_form'),
    path('calculator/', views.calculator_view, name='calculator'),
    path('submit-calculator/', views.submit_calculator, name='submit_calculator'),
]
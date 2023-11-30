from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

urlpatterns = [
    path('menu-items', views.MenuItemsList.as_view(), name='menu-list'),
]

urlpatterns = format_suffix_patterns(urlpatterns)

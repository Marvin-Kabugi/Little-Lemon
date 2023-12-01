from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

urlpatterns = [
    path('menu-items', views.MenuItemsList.as_view(), name='menu-list'),
    path('menu-items/<int:pk>', views.MenuItemsDetail.as_view(), name='menu-item-detail'),
    path('groups/managers/users')
]

urlpatterns = format_suffix_patterns(urlpatterns)

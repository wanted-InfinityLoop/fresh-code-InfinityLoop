from django.urls import path
from .           import views

urlpatterns = [
    path("", views.MenuDetailView.as_view()),
    path("/<int:menu_id>", views.MenuDetailView.as_view()),
    path("/list", views.MenuListView.as_view()),
    path("/item/<int:item_id>", views.MenuItemsView.as_view()),
]


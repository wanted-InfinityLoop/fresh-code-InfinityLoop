from django.urls import path
from .           import views

urlpatterns = [
    path("/<int:menu_id>", views.MenuDetailView.as_view())
]
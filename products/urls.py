from django.urls import path
from .views import PostingProductView, PostingDetailView

urlpatterns = [
    path('/post', PostingProductView.as_view()),
    path('/detail/<int:product_id>', PostingDetailView.as_view()),
]
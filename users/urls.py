from django.urls import path

from users.views import LogInView

urlpatterns = [
    path('/sign-in', LogInView.as_view())
]
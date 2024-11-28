from django.urls import path
from user.views import AuthenticationView

urlpatterns = [
    path("authenticate", AuthenticationView.as_view(), name="authenticate"),
]
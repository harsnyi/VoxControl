from django.urls import path
from home.views import HelloWorldView, GetInfoView, ExecuteCommandView

urlpatterns = [
    path("hello_world", HelloWorldView.as_view(), name="hello_world"),
    path("get_info", GetInfoView.as_view(), name="get_info"),
    path("execute", ExecuteCommandView.as_view(), name="execute")
]

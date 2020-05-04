from django.urls import path
from . import views


urlpatterns = [
    path('', views.handle_file, name="handle_file"),
    path('result', views.show_result, name="show_result")
]

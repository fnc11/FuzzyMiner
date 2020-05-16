from django.urls import path
from . import views


urlpatterns = [
    # path('', views.handle_file, name="handle_file"),
    path('upload', views.upload, name="upload"),
    path('generate', views.show_result, name="generate")
]

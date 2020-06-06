from django.urls import path
from . import views


urlpatterns = [
    # path('', views.handle_file, name="handle_file"),
    path('upload', views.upload, name="upload"),
    path('generate', views.show_result, name="generate"),
    path('node_filter', views.node_filter, name='node_filter'),
    path('edge_filter', views.edge_filter, name='edge_filter'),
    path('concurrency_filter', views.concurrency_filter, name='concurrency_filter'),
    path('metrics', views.metrics_changed, name='metrics')
]

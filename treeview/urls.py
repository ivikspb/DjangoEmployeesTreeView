from django.urls import path
from . import views

urlpatterns = [
    path('', views.treeview, name='treeview'),
    path('api/get', views.treeview_api, name='treeview-api'),
    path('api/get/<int:dip>', views.treeview_api, name='treeview-api'),
    path('api/get/root', views.treeview_root, name='treeview-api-root'),
    path('api/get/detal/<int:eip>', views.treeview_api_detal, name='treeview-api'),
    path('load-all', views.treeview_load_all, name='treeview-all'),
    path('genemployees', views.genemployees, name='genemployees')
]
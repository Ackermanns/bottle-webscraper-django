from django.urls import path
from . import views

#urlconf
urlpatterns = [
    path('', views.home, name=''),
    path('<slug:category>', views.category),
    path('<slug:category>/<slug:item>', views.item),
]
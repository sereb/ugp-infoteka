from django.contrib import admin
from django.urls import path, include
#from infopages import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('infopages.urls'))
    #path('', views.home),
]

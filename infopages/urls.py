from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('kurs', views.kurs, name='kurs'),
    path('step', views.step, name='step'),
    path('about', views.about, name='about'),
    path('login', views.loginpage, name='login'),
    path('stats', views.userstats, name='stats'),
    path('logout', views.logoutpage, name='logout'),
    path('page404', views.page404, name='page404'),
    path('test', views.test, name='test'),
    path('result', views.result, name='result'),
    path('ckeditor/', include('ckeditor_uploader.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

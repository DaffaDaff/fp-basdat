from django.urls import path

from . import views

app_name = 'dashboard'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('edit/', views.edit, name='edit_bio'),
    path('ambil/', views.ambil, name='ambil'),
    path('jadwal/', views.jadwal, name='jadwal'),
    path('kelompok/', views.kelompok, name='kelompok'),
    path('nilai/', views.nilai, name='nilai'),
    path('input-nilai/', views.inputnilai, name='input-nilai'),
    path('jadwal-asisten/', views.jadwalasisten, name='jadwal-asisten')
]

from django.contrib import admin

from .models import Biodata, Praktikan, Praktikum, Asisten, Modul, Kelompok, NilaiPraktikan, Jadwal

# Register your models here.

admin.site.register(Biodata)
admin.site.register(Praktikan)
admin.site.register(Asisten)
admin.site.register(Praktikum)
admin.site.register(Modul)
admin.site.register(NilaiPraktikan)
admin.site.register(Kelompok)
admin.site.register(Jadwal)
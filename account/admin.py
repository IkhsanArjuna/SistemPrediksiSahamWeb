from django.contrib import admin
from .models import Berita

@admin.register(Berita)
class BeritaAdmin(admin.ModelAdmin):
    list_display = ('judul', 'tanggal')  
    search_fields = ('judul',)
    list_filter = ('tanggal',)          

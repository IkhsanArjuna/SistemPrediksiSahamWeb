from django.db import models
from django.contrib.auth.models import User

class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

class Berita(models.Model):
    judul = models.CharField(max_length=255)
    gambar = models.ImageField(upload_to='gambar_berita/')
    link = models.URLField()
    tanggal = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.judul
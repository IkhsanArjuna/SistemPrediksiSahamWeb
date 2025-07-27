from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.register, name='register'),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name='logout'),
    path("home/", views.home, name='home'),
    path("saham/", views.saham, name='saham'),
    path("favorite/", views.favorite, name='favorite'),
    path("addberita/", views.addberita, name='addberita'),
    path("dashboard/", views.dashboard, name='dashboard'),
    path("berita/", views.berita, name='berita'),
    path("bbnipil/", views.bbnipil, name='bbnipil'),
    path("bbripil/", views.bbripil, name='bbripil'),
    path("bbcapil/", views.bbcapil, name='bbcapil'),
    path("unvrpil/", views.unvrpil, name='umvrpil'),
    path("indfpil/", views.indfpil, name='indfpil'),
    path("tlkmpil/", views.tlkmpil, name='tlkmpil'),
    
    # Predict routes
    path('predict_stockbbni7', views.predict_stockbbni7, name='predict_stockbbni7'),
    path('predict_stockbbni30', views.predict_stockbbni30, name='predict_stockbbni30'),
    path('predict_stockbbri7', views.predict_stockbbri7, name='predict_stockbbri7'),
    path('predict_stockbbri30', views.predict_stockbbri30, name='predict_stockbbri30'),
    path('predict_stockbbca7', views.predict_stockbbca7, name='predict_stockbbca7'),
    path('predict_stockbbca30', views.predict_stockbbca30, name='predict_stockbbca30'),
    path('predict_stockunvr7', views.predict_stockunvr7, name='predict_stockunvri7'),
    path('predict_stockunvr30', views.predict_stockunvr30, name='predict_stockunvr30'),
    path('predict_stockindf7', views.predict_stockindf7, name='predict_stockindf7'),
    path('predict_stockindf30', views.predict_stockindf30, name='predict_stockindf30'),
    path('predict_stocktlkm7', views.predict_stocktlkm7, name='predict_stocktlkm7'),
    path('predict_stocktlkm30', views.predict_stocktlkm30, name='predict_stocktlkm30'),

    path('download_forecast_csv/', views.download_forecast_csv, name='download_forecast_csv'),
]

# Tambahkan media URL hanya saat DEBUG = True
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Item
from django.shortcuts import render
from django.http import HttpResponse, FileResponse
from datetime import date
import pandas as pd
import numpy as np
import yfinance as yf
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense, LSTM
import joblib
import plotly.graph_objs as go
from plotly.offline import plot
import io
import tempfile
import os
from django.conf import settings
from django.http import HttpResponse
import plotly.offline as opy
from django.shortcuts import render
from django.http import HttpResponse
from .model_lstm7 import load_data, train_lstm_model, predict_next_7_days, plot_historical, plot_forecast
from .model_lstm30 import load_data, train_lstm_model, predict_next_30_days, plot_historical, plot_forecast
from model_lstm.model_lstm30bbri import load_databbri, train_lstm_modelbbri, predict_next_30_daysbbri, plot_historicalbbri, plot_forecastbbri
from model_lstm.model_lstm7bbri import load_databbri, train_lstm_modelbbri, predict_next_7_daysbbri, plot_historicalbbri, plot_forecastbbri
import plotly.offline as opy
from model_lstm.model_lstm30bbca import load_databbca, train_lstm_modelbbca, predict_next_30_daysbbca, plot_historicalbbca, plot_forecastbbca
from model_lstm.model_lstm7bbca import load_databbca, train_lstm_modelbbca, predict_next_7_daysbbca, plot_historicalbbca, plot_forecastbbca
from model_lstm.model_lstm30unvr import load_dataunvr, train_lstm_modelunvr, predict_next_30_daysunvr, plot_historicalunvr, plot_forecastunvr
from model_lstm.model_lstm7unvr import load_dataunvr, train_lstm_modelunvr, predict_next_7_daysunvr, plot_historicalunvr, plot_forecastunvr
from model_lstm.model_lstm30indf import load_dataindf, train_lstm_modelindf, predict_next_30_daysindf, plot_historicalindf, plot_forecastindf
from model_lstm.model_lstm7indf import load_dataindf, train_lstm_modelindf, predict_next_7_daysindf, plot_historicalindf, plot_forecastindf
from model_lstm.model_lstm30tlkm import load_datatlkm, train_lstm_modeltlkm, predict_next_30_daystlkm, plot_historicaltlkm, plot_forecasttlkm
from model_lstm.model_lstm7tlkm import load_datatlkm, train_lstm_modeltlkm, predict_next_7_daystlkm, plot_historicaltlkm, plot_forecasttlkm
from django.shortcuts import render, redirect
from .forms import BeritaForm
from .models import Berita
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.paginator import Paginator

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
        else:
            user = User.objects.create_user(username=username, password=password)
            user.save()
            messages.success(request, 'Account created successfully')
            return redirect('login')
    return render(request, 'register.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid credentials')
    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return redirect('login')


def saham(request):
    return render(request, 'saham.html')

def favorite(request):
    return render(request, 'favorite-saham.html')

def is_superadmin(user):
    return user.is_superuser

# ADD BERITA - hanya superadmin
@login_required
@user_passes_test(is_superadmin)
def addberita(request):
    if request.method == 'POST':
        form = BeritaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('berita')
    else: 
        form = BeritaForm()
    return render(request, 'add-berita.html', {'form': form})

def dashboard(request):
    return render(request, 'index.html')

def home(request):

    semua = Berita.objects.all().order_by('-tanggal')
    paginator = Paginator(semua, 3)

    page_number = request.GET.get('page')  # ex: ?page=2
    berita_page = paginator.get_page(page_number)

    context = {'semua_berita': berita_page}
    return render(request, 'berita.html', context)

def berita(request):

    semua = Berita.objects.all().order_by('-tanggal')
    paginator = Paginator(semua, 6)

    page_number = request.GET.get('page')  # ex: ?page=2
    berita_page = paginator.get_page(page_number)

    context = {'semua_berita': berita_page}
    return render(request, 'berita.html', context)
def bbnipil(request):
    return render(request, 'bbnipil.html')

def bbripil(request):
    return render(request, 'bbripil.html')

def bbcapil(request):
    return render(request, 'bbcapil.html')

def unvrpil(request):
    return render(request, 'unvrpil.html')

def indfpil(request):
    return render(request, 'indfpil.html')

def tlkmpil(request):
    return render(request, 'tlkmpil.html')

def download_forecast_csv(request):
    file_path = os.path.join(settings.BASE_DIR, 'account', 'data', 'forecast.csv')
    if os.path.exists(file_path):
        return FileResponse(open(file_path, 'rb'), as_attachment=True, filename='forecast.csv')
    return HttpResponse("❌ File CSV tidak ditemukan.")


#Saham BBNI
#Saham BBNI 7 Hari

def predict_stockbbni7(request):
    df = load_data()

    # Validasi data cukup
    if df.empty or len(df) < 61:
        return HttpResponse("❌ Data saham BBNI kosong atau tidak cukup untuk prediksi (minimal 61 baris).")

    # Latih model
    model, scaler, df, scaled_data = train_lstm_model(df)

    # Prediksi 7 hari ke depan
    forecast = predict_next_7_days(model, scaler, df, scaled_data)

    # Simpan ke CSV
    output_dir = os.path.join(settings.BASE_DIR, 'account', 'data')
    os.makedirs(output_dir, exist_ok=True)  # Bikin folder kalau belum ada
    forecast_file_path = os.path.join(output_dir, 'forecast.csv')
    forecast.to_csv(forecast_file_path)
    print(f"✅ Forecast saved to: {forecast_file_path}")

    # Plot historis dan prediksi
    plot1 = plot_historical(df)
    plot2 = plot_forecast(df, forecast)

    # Render grafik ke HTML
    plot1_div = opy.plot(plot1, auto_open=False, output_type='div')
    plot2_div = opy.plot(plot2, auto_open=False, output_type='div')

    context = {
        'plot1': plot1_div,
        'plot2': plot2_div,
        'forecast': forecast.to_html(classes='table table-striped', border=0),
    }

    return render(request, 'bbni7.html', context)


#Saham BBNI 30 Hari 

def predict_stockbbni30(request):
    df = load_data()

    # Validasi data cukup
    if df.empty or len(df) < 61:
        return HttpResponse("❌ Data saham BBNI kosong atau tidak cukup untuk prediksi (minimal 61 baris).")

    # Latih model
    model, scaler, df, scaled_data = train_lstm_model(df)

    # Prediksi 30 hari ke depan
    forecast = predict_next_30_days(model, scaler, df, scaled_data)

    # Simpan ke CSV
    output_dir = os.path.join(settings.BASE_DIR, 'account', 'data')
    os.makedirs(output_dir, exist_ok=True)  # Bikin folder kalau belum ada
    forecast_file_path = os.path.join(output_dir, 'forecast.csv')
    forecast.to_csv(forecast_file_path)
    print(f"✅ Forecast saved to: {forecast_file_path}")

    # Plot historis dan prediksi
    plot1 = plot_historical(df)
    plot2 = plot_forecast(df, forecast)

    # Render grafik ke HTML
    plot1_div = opy.plot(plot1, auto_open=False, output_type='div')
    plot2_div = opy.plot(plot2, auto_open=False, output_type='div')

    context = {
        'plot1': plot1_div,
        'plot2': plot2_div,
        'forecast': forecast.to_html(classes='table table-striped', border=0),
    }

    return render(request, 'bbni30.html', context)



# Saham BBRI
#Saham BBRI 7 Hari

def predict_stockbbri7(request):
    df = load_databbri()

    # Validasi data cukup
    if df.empty or len(df) < 61:
        return HttpResponse("❌ Data saham BBRI kosong atau tidak cukup untuk prediksi (minimal 61 baris).")

    # Latih model
    model, scaler, df, scaled_data = train_lstm_modelbbri(df)

    # Prediksi 7 hari ke depan
    forecast = predict_next_7_daysbbri(model, scaler, df, scaled_data)

    # Simpan ke CSV
    output_dir = os.path.join(settings.BASE_DIR, 'account', 'data')
    os.makedirs(output_dir, exist_ok=True)  # Bikin folder kalau belum ada
    forecast_file_path = os.path.join(output_dir, 'forecast.csv')
    forecast.to_csv(forecast_file_path)
    print(f"✅ Forecast saved to: {forecast_file_path}")

    # Plot historis dan prediksi
    plot1 = plot_historicalbbri(df)
    plot2 = plot_forecastbbri(df, forecast)

    # Render grafik ke HTML
    plot1_div = opy.plot(plot1, auto_open=False, output_type='div')
    plot2_div = opy.plot(plot2, auto_open=False, output_type='div')

    context = {
        'plot1': plot1_div,
        'plot2': plot2_div,
        'forecast': forecast.to_html(classes='table table-striped', border=0),
    }

    return render(request, 'bbri7.html', context)


#Saham BBRI 30 Hari 

def predict_stockbbri30(request):
    df = load_databbri()

    # Validasi data cukup
    if df.empty or len(df) < 61:
        return HttpResponse("❌ Data saham BBRI kosong atau tidak cukup untuk prediksi (minimal 61 baris).")

    # Latih model
    model, scaler, df, scaled_data = train_lstm_modelbbri(df)

    # Prediksi 30 hari ke depan
    forecast = predict_next_30_daysbbri(model, scaler, df, scaled_data)

    # Simpan ke CSV
    output_dir = os.path.join(settings.BASE_DIR, 'account', 'data')
    os.makedirs(output_dir, exist_ok=True)  # Bikin folder kalau belum ada
    forecast_file_path = os.path.join(output_dir, 'forecast.csv')
    forecast.to_csv(forecast_file_path)
    print(f"✅ Forecast saved to: {forecast_file_path}")

    # Plot historis dan prediksi
    plot1 = plot_historicalbbri(df)
    plot2 = plot_forecastbbri(df, forecast)

    # Render grafik ke HTML
    plot1_div = opy.plot(plot1, auto_open=False, output_type='div')
    plot2_div = opy.plot(plot2, auto_open=False, output_type='div')

    context = {
        'plot1': plot1_div,
        'plot2': plot2_div,
        'forecast': forecast.to_html(classes='table table-striped', border=0),
    }

    return render(request, 'bbri30.html', context)


# Saham BBCA
#Saham BBCA 7 Hari

def predict_stockbbca7(request):
    df = load_databbca()

    # Validasi data cukup
    if df.empty or len(df) < 61:
        return HttpResponse("❌ Data saham BB kosong atau tidak cukup untuk prediksi (minimal 61 baris).")

    # Latih model
    model, scaler, df, scaled_data = train_lstm_modelbbca(df)

    # Prediksi 7 hari ke depan
    forecast = predict_next_7_daysbbca(model, scaler, df, scaled_data)

    # Simpan ke CSV
    output_dir = os.path.join(settings.BASE_DIR, 'account', 'data')
    os.makedirs(output_dir, exist_ok=True)  # Bikin folder kalau belum ada
    forecast_file_path = os.path.join(output_dir, 'forecast.csv')
    forecast.to_csv(forecast_file_path)
    print(f"✅ Forecast saved to: {forecast_file_path}")

    # Plot historis dan prediksi
    plot1 = plot_historicalbbca(df)
    plot2 = plot_forecastbbca(df, forecast)

    # Render grafik ke HTML
    plot1_div = opy.plot(plot1, auto_open=False, output_type='div')
    plot2_div = opy.plot(plot2, auto_open=False, output_type='div')

    context = {
        'plot1': plot1_div,
        'plot2': plot2_div,
        'forecast': forecast.to_html(classes='table table-striped', border=0),
    }

    return render(request, 'bbca7.html', context)


#Saham BBRI 30 Hari 

def predict_stockbbca30(request):
    df = load_databbca()

    # Validasi data cukup
    if df.empty or len(df) < 61:
        return HttpResponse("❌ Data saham BBCA kosong atau tidak cukup untuk prediksi (minimal 61 baris).")

    # Latih model
    model, scaler, df, scaled_data = train_lstm_modelbbca(df)

    # Prediksi 30 hari ke depan
    forecast = predict_next_30_daysbbca(model, scaler, df, scaled_data)

    # Simpan ke CSV
    output_dir = os.path.join(settings.BASE_DIR, 'account', 'data')
    os.makedirs(output_dir, exist_ok=True)  # Bikin folder kalau belum ada
    forecast_file_path = os.path.join(output_dir, 'forecast.csv')
    forecast.to_csv(forecast_file_path)
    print(f"✅ Forecast saved to: {forecast_file_path}")

    # Plot historis dan prediksi
    plot1 = plot_historicalbbca(df)
    plot2 = plot_forecastbbca(df, forecast)

    # Render grafik ke HTML
    plot1_div = opy.plot(plot1, auto_open=False, output_type='div')
    plot2_div = opy.plot(plot2, auto_open=False, output_type='div')

    context = {
        'plot1': plot1_div,
        'plot2': plot2_div,
        'forecast': forecast.to_html(classes='table table-striped', border=0),
    }

    return render(request, 'bbca30.html', context)

# Saham UNVR
#Saham UNVR 7 Hari

def predict_stockunvr7(request):
    df = load_dataunvr()

    # Validasi data cukup
    if df.empty or len(df) < 61:
        return HttpResponse("❌ Data saham UNVR kosong atau tidak cukup untuk prediksi (minimal 61 baris).")

    # Latih model
    model, scaler, df, scaled_data = train_lstm_modelunvr(df)

    # Prediksi 7 hari ke depan
    forecast = predict_next_7_daysunvr(model, scaler, df, scaled_data)

    # Simpan ke CSV
    output_dir = os.path.join(settings.BASE_DIR, 'account', 'data')
    os.makedirs(output_dir, exist_ok=True)  # Bikin folder kalau belum ada
    forecast_file_path = os.path.join(output_dir, 'forecast.csv')
    forecast.to_csv(forecast_file_path)
    print(f"✅ Forecast saved to: {forecast_file_path}")

    # Plot historis dan prediksi
    plot1 = plot_historicalunvr(df)
    plot2 = plot_forecastunvr(df, forecast)

    # Render grafik ke HTML
    plot1_div = opy.plot(plot1, auto_open=False, output_type='div')
    plot2_div = opy.plot(plot2, auto_open=False, output_type='div')

    context = {
        'plot1': plot1_div,
        'plot2': plot2_div,
        'forecast': forecast.to_html(classes='table table-striped', border=0),
    }

    return render(request, 'unvr7.html', context)


#Saham UNVR 30 Hari 

def predict_stockunvr30(request):
    df = load_dataunvr()

    # Validasi data cukup
    if df.empty or len(df) < 61:
        return HttpResponse("❌ Data saham UNVR kosong atau tidak cukup untuk prediksi (minimal 61 baris).")

    # Latih model
    model, scaler, df, scaled_data = train_lstm_modelunvr(df)

    # Prediksi 30 hari ke depan
    forecast = predict_next_30_daysunvr(model, scaler, df, scaled_data)

    # Simpan ke CSV
    output_dir = os.path.join(settings.BASE_DIR, 'account', 'data')
    os.makedirs(output_dir, exist_ok=True)  # Bikin folder kalau belum ada
    forecast_file_path = os.path.join(output_dir, 'forecast.csv')
    forecast.to_csv(forecast_file_path)
    print(f"✅ Forecast saved to: {forecast_file_path}")

    # Plot historis dan prediksi
    plot1 = plot_historicalunvr(df)
    plot2 = plot_forecastunvr(df, forecast)

    # Render grafik ke HTML
    plot1_div = opy.plot(plot1, auto_open=False, output_type='div')
    plot2_div = opy.plot(plot2, auto_open=False, output_type='div')

    context = {
        'plot1': plot1_div,
        'plot2': plot2_div,
        'forecast': forecast.to_html(classes='table table-striped', border=0),
    }

    return render(request, 'unvr30.html', context)

#Saham INDF
#Saham INDF 7 Hari

def predict_stockindf7(request):
    df = load_dataindf()

    # Validasi data cukup
    if df.empty or len(df) < 61:
        return HttpResponse("❌ Data saham INDF kosong atau tidak cukup untuk prediksi (minimal 61 baris).")

    # Latih model
    model, scaler, df, scaled_data = train_lstm_modelindf(df)

    # Prediksi 7 hari ke depan
    forecast = predict_next_7_daysindf(model, scaler, df, scaled_data)

    # Simpan ke CSV
    output_dir = os.path.join(settings.BASE_DIR, 'account', 'data')
    os.makedirs(output_dir, exist_ok=True)  # Bikin folder kalau belum ada
    forecast_file_path = os.path.join(output_dir, 'forecast.csv')
    forecast.to_csv(forecast_file_path)
    print(f"✅ Forecast saved to: {forecast_file_path}")

    # Plot historis dan prediksi
    plot1 = plot_historicalindf(df)
    plot2 = plot_forecastindf(df, forecast)

    # Render grafik ke HTML
    plot1_div = opy.plot(plot1, auto_open=False, output_type='div')
    plot2_div = opy.plot(plot2, auto_open=False, output_type='div')

    context = {
        'plot1': plot1_div,
        'plot2': plot2_div,
        'forecast': forecast.to_html(classes='table table-striped', border=0),
    }

    return render(request, 'indf7.html', context)


#Saham INDF 30 Hari 

def predict_stockindf30(request):
    df = load_dataindf()

    # Validasi data cukup
    if df.empty or len(df) < 61:
        return HttpResponse("❌ Data saham INDF kosong atau tidak cukup untuk prediksi (minimal 61 baris).")

    # Latih model
    model, scaler, df, scaled_data = train_lstm_modelindf(df)

    # Prediksi 30 hari ke depan
    forecast = predict_next_30_daysindf(model, scaler, df, scaled_data)

    # Simpan ke CSV
    output_dir = os.path.join(settings.BASE_DIR, 'account', 'data')
    os.makedirs(output_dir, exist_ok=True)  # Bikin folder kalau belum ada
    forecast_file_path = os.path.join(output_dir, 'forecast.csv')
    forecast.to_csv(forecast_file_path)
    print(f"✅ Forecast saved to: {forecast_file_path}")

    # Plot historis dan prediksi
    plot1 = plot_historicalindf(df)
    plot2 = plot_forecastindf(df, forecast)

    # Render grafik ke HTML
    plot1_div = opy.plot(plot1, auto_open=False, output_type='div')
    plot2_div = opy.plot(plot2, auto_open=False, output_type='div')

    context = {
        'plot1': plot1_div,
        'plot2': plot2_div,
        'forecast': forecast.to_html(classes='table table-striped', border=0),
    }

    return render(request, 'indf30.html', context)


#Saham TLKM
#Saham TLKM 7 Hari

def predict_stocktlkm7(request):
    df = load_datatlkm()

    # Validasi data cukup
    if df.empty or len(df) < 61:
        return HttpResponse("❌ Data saham TLKM kosong atau tidak cukup untuk prediksi (minimal 61 baris).")

    # Latih model
    model, scaler, df, scaled_data = train_lstm_modeltlkm(df)

    # Prediksi 7 hari ke depan
    forecast = predict_next_7_daystlkm(model, scaler, df, scaled_data)

    # Simpan ke CSV
    output_dir = os.path.join(settings.BASE_DIR, 'account', 'data')
    os.makedirs(output_dir, exist_ok=True)  # Bikin folder kalau belum ada
    forecast_file_path = os.path.join(output_dir, 'forecast.csv')
    forecast.to_csv(forecast_file_path)
    print(f"✅ Forecast saved to: {forecast_file_path}")

    # Plot historis dan prediksi
    plot1 = plot_historicaltlkm(df)
    plot2 = plot_forecasttlkm(df, forecast)

    # Render grafik ke HTML
    plot1_div = opy.plot(plot1, auto_open=False, output_type='div')
    plot2_div = opy.plot(plot2, auto_open=False, output_type='div')

    context = {
        'plot1': plot1_div,
        'plot2': plot2_div,
        'forecast': forecast.to_html(classes='table table-striped', border=0),
    }

    return render(request, 'tlkm7.html', context)


#Saham BBNI 30 Hari 

def predict_stocktlkm30(request):
    df = load_datatlkm()

    # Validasi data cukup
    if df.empty or len(df) < 61:
        return HttpResponse("❌ Data saham TLKM kosong atau tidak cukup untuk prediksi (minimal 61 baris).")

    # Latih model
    model, scaler, df, scaled_data = train_lstm_modeltlkm(df)

    # Prediksi 30 hari ke depan
    forecast = predict_next_30_daystlkm(model, scaler, df, scaled_data)

    # Simpan ke CSV
    output_dir = os.path.join(settings.BASE_DIR, 'account', 'data')
    os.makedirs(output_dir, exist_ok=True)  # Bikin folder kalau belum ada
    forecast_file_path = os.path.join(output_dir, 'forecast.csv')
    forecast.to_csv(forecast_file_path)
    print(f"✅ Forecast saved to: {forecast_file_path}")

    # Plot historis dan prediksi
    plot1 = plot_historicaltlkm(df)
    plot2 = plot_forecasttlkm(df, forecast)

    # Render grafik ke HTML
    plot1_div = opy.plot(plot1, auto_open=False, output_type='div')
    plot2_div = opy.plot(plot2, auto_open=False, output_type='div')

    context = {
        'plot1': plot1_div,
        'plot2': plot2_div,
        'forecast': forecast.to_html(classes='table table-striped', border=0),
    }

    return render(request, 'tlkm30.html', context)






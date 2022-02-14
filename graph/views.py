from turtle import width
from unicodedata import name
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import authenticate, login
from .models import GraphModel
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView, PasswordChangeView
from django.views.generic import CreateView
from django.http import HttpResponseRedirect
import plotly.graph_objects as go
from plotly.offline import plot
import plotly.express as px
import datetime
from pandas_datareader import data
import pandas as pd
from plotly.offline import plot
import numpy as np

def signupview(request):
    if request.method == 'POST':
        username=request.POST['username_data']
        password=request.POST['password_data']
        try:
            user=User.objects.create_user(username,'',password)
            return render(request, 'signup.html', {"success":"登録しました。"})
        except IntegrityError:
            return render(request, 'signup.html',{'error':'このユーザーは既に登録されています。'})
    else:
        return render(request, 'signup.html')
    

def loginview(request):
    if request.method=='POST':
        username_data=request.POST.get('username_data')
        password_data=request.POST.get('password_data')
        user = authenticate(username=username_data, password=password_data)
        print(user)
        if user:
            login(request,user)
            return HttpResponseRedirect(reverse('list'))
        else:
            return render(request, 'login.html', {'error':"アカウント作ってないでしょ!!"})
    else:
        return render(request,'login.html')

@login_required
def listview(request):
    object_list=GraphModel.objects.all()
    return render(request,'list.html',{'object_list':object_list})


class logoutview(LogoutView):
    template_name='logout.html'
    

class passwordview(PasswordChangeView):
    template_name='changepassword.html'
    success_url=reverse_lazy('login')

def graphview(request):
    i=0
    L=0
    data_x=[]
    data_y=[]
    df = GraphModel.objects.all()
    L=len(df)

    for i in range(L):
        data_x.append(df[i].title)
        data_y.append(df[i].Revenue)
        i=i+1
    print(data_x,data_y)
    fig=px.bar(x=data_x,y=data_y)
    
    plot_fig = plot(fig, output_type='div', include_plotlyjs=False)
    return render(request, 'index.html',{'graph':plot_fig})

class creatclass(CreateView):
    template_name='create.html'
    model=GraphModel
    today=datetime.date.today()
    fields=('title','Date','Revenue','author')
    success_url=reverse_lazy('graph')

def stock(request):
    start = "2021-01-01"
    end = "2021-12-31"
    code="TSLA"
    apikey="E5HBS439W6ESE9LT"
    df=data.DataReader(code,'av-daily',start,end,api_key=apikey)
    date=df.index
    price=df['close']
    fig=go.Figure()
    fig.add_trace(go.Scatter(x=date,y=price,mode='lines',name='Tesla'))
    fig.update_layout(title="<b>The price of Tesla's stock",xaxis=dict(title='日付'),yaxis=dict(title='株価($)'))
    plot_fig=plot(fig, output_type='div', include_plotlyjs=False)
    return render(request, 'index.html',{'graph':plot_fig})
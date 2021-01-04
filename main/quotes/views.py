from django.shortcuts import render, redirect
# from django.http import HttpResponse
from .models import Stock
from .forms import StockForm, SignUpForm, EditProfileForm
from django.contrib import messages
# from django.views.generic import TemplateView
import io
import urllib
import base64
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm


def add(x, y):
    return x + y


def home(request):
    import requests
    import json
    import matplotlib.pyplot as plt

    if request.method == "POST":
        ticker = request.POST["ticker"]
        api_request = requests.get(
            "https://sandbox.iexapis.com/stable/stock/"
            + ticker
            + "/quote?token=Tpk_1ffd0fa5cbb241889288941e2f4e0e0f"
        )
        try:
            api = json.loads(api_request.content)
            plt.switch_backend('agg')
            plt.plot([15, 16, 17, 22], [api.get('open'), api.get('low'), api.get('high'), api.get('close')])
            plt.ylabel('P R I C E I N $')
            plt.xlabel('TIME')
            fig = plt.gcf()
            buf = io.BytesIO()
            fig.savefig(buf, format="png")
            buf.seek(0)
            string = base64.b64encode(buf.read())
            uri = urllib.parse.quote(string)
        except Exception as e:
            api = "Error..."
        return render(request, "home.html", {"data": uri})
    else:
        return render(request, "home.html", {"ticker": "Enter a ticker symbol above"})


def add_stock(request):
    import requests
    import json

    if request.method == "POST":
        form = StockForm(request.POST or None)

        if form.is_valid():
            form.save()
            messages.success(request, ("Stock Has Been Added..."))
            return redirect("add_stock")
    else:
        ticker = Stock.objects.all()
        output = []
        for ticker_item in ticker:
            api_request = requests.get(
                "https://sandbox.iexapis.com/stable/stock/"
                + str(ticker_item)
                + "/quote?token=Tpk_1ffd0fa5cbb241889288941e2f4e0e0f"
            )
            try:
                api = json.loads(api_request.content)
                output.append(api)
            except Exception as e:
                api = "Error..."

        return render(request, "stocktemp/add_stock.html", {"ticker": ticker, "output": output})


def delete(request, stock_id):

    item = Stock.objects.get(pk=stock_id)
    item.delete()
    messages.success(request, ("Stock Has Been Deleted!"))
    return redirect(delete_stock)


def delete_stock(request):

    ticker = Stock.objects.all()
    return render(request, "stocktemp/delete_stock.html", {"ticker": ticker})


def login_user(request):

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, ("You Have Logged in"))
            return redirect('home')
        else:
            messages.success(request, ("error Logged in"))
            return redirect('login')
    else:
        return render(request, 'usertemp/login.html')


def logout_user(request):

    logout(request)
    messages.success(request, ('You Haver Been Logged Out...'))
    return redirect('home')


def change_password(request):

    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, ('You Have Edited Your Password...'))
            return redirect('home')
    else:
        form = PasswordChangeForm(user=request.user)
    context = {'form': form}
    return render(request, 'usertemp/change_password.html', context)


def edit_profile(request):

    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, ('You Have Edited Your Profile...'))
            return redirect('home')
    else:
        form = EditProfileForm(instance=request.user)
    context = {'form': form}
    return render(request, 'usertemp/edit_profile.html', context)


def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ('You Have Been Registered...'))
            return redirect('home')
    else:
        form = SignUpForm()

    context = {'form': form}
    return render(request, 'usertemp/register.html', context)

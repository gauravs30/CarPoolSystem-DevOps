from django.shortcuts import render
from decimal import Decimal

# Create your views here.
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import User, Car, Book
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .forms import UserLoginForm, UserRegisterForm
from django.contrib.auth.decorators import login_required
from decimal import Decimal


import io
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.template import Context


def home(request):
    if request.user.is_authenticated:
        return render(request, 'myapp/home.html')
    else:
        return render(request, 'myapp/signin.html')


@login_required(login_url='signin')
def findcar(request):
    context = {}
    if request.method == 'POST':
        source_r = request.POST.get('source')
        dest_r = request.POST.get('destination')
        date_r = request.POST.get('date')
        car_list = Car.objects.filter(source=source_r, dest=dest_r, date=date_r)
        if car_list:
            return render(request, 'myapp/list.html', locals())
        else:
            context["error"] = "Sorry no cars available for pooling"
            return render(request, 'myapp/findcar.html', context)
    else:
        return render(request, 'myapp/findcar.html')


@login_required(login_url='signin')
def bookings(request):
    context = {}
    if request.method == 'POST':
        id_r = request.POST.get('car_id')
        seats_r = int(request.POST.get('no_seats'))
        obj_car = Car.objects.get(id=id_r)
        if obj_car:
            if obj_car.rem > int(seats_r):
                name_r = obj_car.car_name
                cost = int(seats_r) * obj_car.price
                source_r = obj_car.source
                dest_r = obj_car.dest
                nos_r = Decimal(obj_car.nos)
                price_r = obj_car.price
                date_r = obj_car.date
                time_r = obj_car.time
                username_r = request.user.username
                email_r = request.user.email
                userid_r = request.user.id
                rem_r = obj_car.rem - seats_r
                Car.objects.filter(id=id_r).update(rem=rem_r)
                book = Book.objects.create(name=username_r, email=email_r, userid=userid_r, car_name=name_r,
                                           source=source_r, carid=id_r,
                                           dest=dest_r, price=price_r, nos=seats_r, date=date_r, time=time_r,
                                           status='BOOKED')
                print('------------book id-----------', book.id)
                # book.save()
                return render(request, 'myapp/bookings.html', locals())
            else:
                context["error"] = "Sorry select fewer number of seats"
                return render(request, 'myapp/findcar.html', context)

    else:
        return render(request, 'myapp/findcar.html')


@login_required(login_url='signin')
def cancellings(request):
    context = {}
    if request.method == 'POST':
        id_r = request.POST.get('car_id')
        #seats_r = int(request.POST.get('no_seats'))

        try:
            book = Book.objects.get(id=id_r)
            car = Car.objects.get(id=book.carid)
            rem_r = car.rem + book.nos
            Car.objects.filter(id=book.carid).update(rem=rem_r)
            #nos_r = book.nos - seats_r
            Book.objects.filter(id=id_r).update(status='CANCELLED')
            Book.objects.filter(id=id_r).update(nos=0)
            return redirect(seebookings)
        except Book.DoesNotExist:
            context["error"] = "Sorry You have not booked that Car"
            return render(request, 'myapp/error.html', context)
    else:
        return render(request, 'myapp/findcar.html')


@login_required(login_url='signin')
def seebookings(request, new={}):
    context = {}
    id_r = request.user.id
    book_list = Book.objects.filter(userid=id_r)
    if book_list:
        return render(request, 'myapp/booklist.html', locals())
    else:
        context["error"] = "Sorry no cars booked"
        return render(request, 'myapp/findcar.html', context)


@login_required(login_url='signin')
def deleterecord(request):
    context = {}
    if request.method == 'POST':
        id_r = request.POST.get('car_id')
        try:
            book = Book.objects.get(id=id_r)
            car = Car.objects.get(id=book.carid)
            rem_r = car.rem + book.nos
            Car.objects.filter(id=book.carid).update(rem=rem_r)
            Book.objects.filter(id=id_r).delete()
            Book.objects.filter(id=id_r).update(nos=0)
            return redirect(seebookings)

        except Book.DoesNotExist:
            context["error"] = "Sorry You have not booked "
            return render(request, 'myapp/error.html', context)
    else:
        return render(request, 'myapp/findcar.html')


def signup(request):
    context = {}
    if request.method == 'POST':
        name_r = request.POST.get('name')
        email_r = request.POST.get('email')
        password_r = request.POST.get('password')
        user = User.objects.create_user(name_r, email_r, password_r, )
        if user:
            login(request, user)
            return render(request, 'myapp/thank.html')
        else:
            context["error"] = "Provide valid credentials"
            return render(request, 'myapp/signup.html', context)
    else:
        return render(request, 'myapp/signup.html', context)


def signin(request):
    context = {}
    if request.method == 'POST':
        name_r = request.POST.get('name')
        password_r = request.POST.get('password')
        user = authenticate(request, username=name_r, password=password_r)
        if user:
            login(request, user)
            # username = request.session['username']
            context["user"] = name_r
            context["id"] = request.user.id
            return render(request, 'myapp/success.html', context)
            # return HttpResponseRedirect('success')
        else:
            context["error"] = "Provide valid credentials"
            return render(request, 'myapp/signin.html', context)
    else:
        context["error"] = "You are not logged in"
        return render(request, 'myapp/signin.html', context)


def signout(request):
    context = {}
    logout(request)
    context['error'] = "You have been logged out"
    return render(request, 'myapp/signin.html', context)


def success(request):
    context = {}
    context['user'] = request.user
    return render(request, 'myapp/success.html', context)

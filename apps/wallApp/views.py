from django.shortcuts import render, HttpResponse, redirect
from .models import *
import bcrypt
import datetime
# Create your views here.
#///////////////////////////////////////////////
#RENDER ROUTES
#///////////////////////////////////////////////
def index(request):
    if 'id' in request.session:
        return redirect('/dashboard')
    return render(request,'wallApp/home.html')
    
def login_page(request):
    if 'id' in request.session:
        return redirect('/dashboard')
    return render(request,'wallApp/signin.html')
def register_page(request):
    if 'id' in request.session:
        return redirect('/dashboard')
    return render(request,'wallApp/register.html')

def dashboard_page(request):
    if 'id' in request.session:
        data={
            'id': request.session['id'],
            'users': User.objects.all()
        }
        
        return render(request,'wallApp/dashboard.html', data)
    else:
        return redirect('/')

#///////////////////////////////////////////////
#PROCESS
#///////////////////////////////////////////////
def login_process(request):
    if 'id' in request.session:
        return redirect('/dashboard')
    if request.method =='POST':
        users = User.objects.filter(email=request.POST['email'])
        if len(users):
            if bcrypt.checkpw(request.POST['password'].encode(), users[0].password_hash.encode()):
                request.session['id'] = users[0].id
                return redirect('/dashboard')
    print("OH SHIE")
    return redirect('/login')

def register_process(request):
    if 'id' in request.session:
        return redirect('/dashboard')
    if request.method =='POST':
        errors = User.objects.info_validation(request.POST)
        if len(errors):
            for key, value in errors.items():
                print(key, value)
        else:
            pw_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
            birthday = datetime.date(month=int(request.POST['month']),day=int(request.POST['day']),year=int(request.POST['year']))

            new_user = User.objects.create(
                first_name = request.POST['first_name'],
                last_name = request.POST['last_name'],
                email = request.POST['email'],
                password_hash =  pw_hash,
                birthday = birthday
            )
            request.session['id'] = new_user.id
            return redirect('/dashboard')
    return redirect('/register')

def logout_process(request):
    if 'id' in request.session:
        request.session.clear()

    return redirect('/')
    
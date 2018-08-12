import datetime
from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
import bcrypt
from .models import *

"""RENDER ROUTES"""

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
        # CHECK FOR VALID ID
        users = User.objects.filter(id=request.session['id'])
        if len(users):
            data = {'id': request.session['id'],
                    'users': User.objects.all()}
            # IF USER NOT ADMIN
            if users[0].user_level == 9:
                return redirect('/admin')
            else:
                data['self'] = users[0]
                return render(request,'wallApp/dashboard.html', data)
    
    return redirect('/')

def admin_page(request):
    if 'id' in request.session:
        # CHECK FOR VALID ID
        users = User.objects.filter(id=request.session['id'])
        if len(users) and users[0].user_level ==9:
            data = {'id': request.session['id'],
                    'users': User.objects.all()}
            data['self'] = users[0]
            return render(request,'wallApp/admin.html', data)
    
    return redirect('/')

def profile_page(request, id):
    # IF VISITOR IS LOGGED IN
    if 'id' in request.session:
        # CHECK IF PAGE OWNER'S ID IS VALID
        users = User.objects.filter(id=id)
        if len(users):
            data = {'owner' : users[0],
                    'visitor' : User.objects.get(id=users[0].id)}
            return render(request,'wallApp/profile.html', data)
    return redirect('/')

def user_edit_page(request):
    if 'id' in request.session:
        users = User.objects.filter(id=request.session['id'])
        if len(users) and users[0].user_level == 1:
                data = { 'user' : User.objects.get(id=users[0].id) }
                return render(request, 'wallApp/edit.html', data)
    return redirect('/')

def admin_edit_page(request,id):
    # IF USER IS LOGGED IN AS ADMIN
    if 'id' in request.session:
        users = User.objects.filter(id=request.session['id'])
        if len(users) and users[0].user_level == 9:
                data={  
                    'user' : User.objects.get(id=id)
                }
                return render(request, 'wallApp/editadmin.html', data)
    return redirect('/')

"""PROCESS ROUTES"""

def login_process(request):
    if 'id' in request.session:
        return redirect('/dashboard')
    if request.method =='POST':
        users = User.objects.filter(email=request.POST['email'])
        if len(users):
            if bcrypt.checkpw(request.POST['password'].encode(), users[0].password_hash.encode()):
                request.session['id'] = users[0].id
                return redirect('/dashboard')
    messages.error(request, "Your email/password is incorrect.")
    return redirect('/login')

def register_process(request):
    if 'id' in request.session:
        return redirect('/dashboard')
    if request.method =='POST':
        errors = User.objects.info_validation(request.POST, check_all=True)
        if len(errors):
            for key, value in errors.items():
                print(value)
                messages.error(request, value)
        else:
            pw_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
            birthday = datetime.date(
                month=int(request.POST['month']),
                day=int(request.POST['day']),
                year=int(request.POST['year']))

            new_user = User.objects.create(
                first_name = request.POST['first_name'],
                last_name = request.POST['last_name'],
                email = request.POST['email'],
                password_hash =  pw_hash,
                birthday = birthday,)
            request.session['id'] = new_user.id
            return redirect('/dashboard')
    return redirect('/register')

def logout_process(request):
    if 'id' in request.session:
        request.session.clear()

    return redirect('/')

def message_process(request,id):
    # IF USER GOT HERE VIA POST AND IS LOGGED IN
    if request.method == 'POST' and 'id' in request.session:
        # IF TARGET'S ID IS CORRECT
        users = User.objects.filter(id=id)
        if len(users):
            if len(request.POST['content']) == 0:
                messages.error(request,"Message can't be empty")
            else:
                sender = User.objects.get(id=request.session['id'])
                Message.objects.create(
                    content=request.POST['content'], 
                    sender=sender, 
                    receiver=users[0]
                )
                return redirect('/users/'+str(id)+'/')
    return redirect('/')

def comment_process(request, msg_id):
    if request.method == 'POST' and 'id' in request.session:
        messages = Message.objects.filter(id=msg_id)
        if len(messages):
            print(request.POST)
            if len(request.POST['content']) == 0:
                messages.error(request,"Comment can't be empty")
            else:
                commenter = User.objects.get(id=request.session['id'])
                new_comment = Comment.objects.create(
                    content=request.POST['content'], 
                    commenter=commenter, 
                    message=messages[0])
                page_id = new_comment.message.receiver.id
                
            return redirect('/users/'+str(page_id)+'/')
    return redirect('/')

def edit_process(request,id):
    # CHECK IF EDITOR IS LOGGED IN W/ VALID ID
    if request.method == 'POST' and 'id' in request.session:
        editors = User.objects.filter(id=request.session['id'])
        targets = User.objects.filter(id=id)
        if len(editors) and len(targets):
            # If user trying to edit own page or is admin
            if editors[0].id == id or editors[0].user_level == 9:
                # If user trying to edit personal info
                if 'first_name' in request.POST and 'last_name' in request.POST and 'email' in request.POST:
                    if 'user_level' in request.POST and editors[0].user_level == 9:
                        user_level = int(request.POST['user_level'])
                    else: 
                        user_level = 1
                    
                    errors = User.objects.info_validation(
                        request.POST, 
                        check_name=True, 
                        check_email_format=True)
                    if len(errors):
                        for key, value in errors.items():
                            messages.error(request, value)
                        
                    else:
                        targets.update(
                            first_name = request.POST['first_name'],
                            last_name = request.POST['last_name'],
                            email = request.POST['email'],
                            user_level = user_level
                        )
                # If user trying to update password
                elif 'password' in request.POST:
                    errors = User.objects.info_validation(request.POST, check_password=True)
                    if len(errors):
                        for key, value in errors.items():
                            messages.error(request, value)
                    else:
                        pw_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
                        targets.update(password_hash=pw_hash)

                return redirect('/admin/'+str(id)+'/edit')
    return redirect('/')
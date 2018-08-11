from django.shortcuts import render, HttpResponse

# Create your views here.
def index(request):
    return render(request,'wallApp/home.html')
def login_page(request):
    return render(request,'wallApp/signin.html')
def register_page(request):
    return render(request,'wallApp/register.html')
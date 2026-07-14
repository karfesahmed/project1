from django.shortcuts import render
from django.contrib.auth import authenticate,login,logout
from django.shortcuts import redirect
# Create your views here.

def login_view(request):
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            return redirect("home")
        else:
            return render(request,'dashboard/login.html',{
                "message":"invalid username or password"
            })
    return render(request,'dashboard/login.html')
def logout_view(request):
    logout(request)
    return redirect("home")
from django.shortcuts import render
from django.contrib import messages, auth
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
# Create your views here.

# function to test if user is logged out or not
def notloggedin(user):
    if user.is_authenticated:
        return False
    else:
        return True


# only allow logged out users to view this page else redirect to dashboard page
@user_passes_test(notloggedin, login_url='coreapp')
def index(request):
    return render(request, "accounts/index.html")

# only allow logged out users to view this page else redirect to dashboard page
@user_passes_test(notloggedin, login_url='coreapp')
def login(request):
    if request.method == 'POST':
        #Login User
        usernamevalue = request.POST['username']
        username = usernamevalue.lower()
        password = request.POST['password']
        print(username)

       
        user = auth.authenticate(username=username, password=password)
        
        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are now logged in')
            return redirect('coreapp')
    
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('login')
    else:
     return render(request, 'accounts/login.html')

@login_required(login_url='login')
def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request, 'You are logged out')
        return redirect('login')
    
    

from django.shortcuts import render
from django.contrib import messages, auth
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
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
    
    
@user_passes_test(notloggedin, login_url='coreapp')
def register(request):
    if request.method == 'POST':
        charsToCheck = ['@', '/', '.', '+', '-', '/', '_', ',', ' ', r"'", r'"']
        namesCheck = ['@', '/', '.', '+', '-', '/', '_', ',', r"'", r'"']
        # Get Form Values
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        usernamevalue = request.POST['username']
        username = usernamevalue.lower()
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        # is_uni = request.POST.getlist('is_uni')
        # print(is_uni)

        # Check if passwords match

        if password == password2:
            #check username
            if User.objects.filter(username=username).exists():
                messages.error(request, 'That username is already taken')
                return redirect('index')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'That email is already taken')
                    return redirect('index')
                else:
                    if any(c in username for c in charsToCheck):
                        messages.error(request, "Only alphabets and numbers are allowed in your username with no spacing")
                        return redirect('index')
                    
                    else:
                        if any(c in first_name for c in namesCheck):
                            messages.error(request, "Please enter valid characters for your first name")
                            return redirect('index')
                    
                        else:
                            if any(c in last_name for c in namesCheck):
                                messages.error(request, "Please enter valid characters for your last name")
                                return redirect('index')
                    
                            else:
                                # Looks good
                                user = User.objects.create_user(username=username.lower(), password=password, email=email, first_name=first_name, last_name=last_name)
                                user.save()
                                auth.login(request, user)
                                messages.success(request, 'You are now registered and logged in!')
                                return render(request, 'coreapp/dashboard.html')
        else:
            messages.error(request, 'Passwords do not match')
            return redirect('index')
    else:
        return render(request, 'accounts/index.html')

## This page is to be shown in the event of page crashes

def handle_404(request, exception):
    return render(request, 'accounts/helpers/notfound404.html', status=404)

def handle_500(request,*args, **argv):
    return render(request, 'accounts/helpers/notfound500.html', status=500)
    
def csrf_failure(request, *args, **argv):
    return render(request, 'accounts/helpers/missingcsrf.html', status=403)
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, UserManager
from .models import Wish, WishManager

# Requirements for LOGIN: validations
# login portion
def index(request):
    return render(request,'login.html')

def register(request):
    errors = User.objects.validator(request.POST)
    print(errors)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    print(request.POST['password'])
    new_user = User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=request.POST['password'])
    print(new_user)
    request.session['user'] = new_user.id
    return redirect('/wishes')

def login(request):
    errors = User.objects.login_validator(request.POST)
    print(errors)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    print(request.POST['password'])
    logged_user = User.objects.filter(email=request.POST['email'])
    print(logged_user)
    if len(logged_user) > 0:
        if request.POST['password'] == logged_user[0].password:
            request.session['user'] = logged_user[0].id
            return redirect('/wishes')

# Wishing App Views portion
# make def wishes "dashboard" aka main page
# Display wishes made by CURRENT user that have been WISHES FOR and GRANTED 
def wishes(request):
    if 'user' not in request.session:
        return redirect('/')
    else:
        context = {
            'wishes': Wish.objects.all(),
            'current_user': User.objects.get(id=request.session['user'])
        }
    return render(request,'dashboard.html',context)

# Make a new html to create a new wish
def new_wish(request):
    context ={
        'current_user': User.objects.get(id=request.session['user'])
    }
    return render(request,'new_wish.html',context)

# make the validator show up!! 
# create a new wish
def create_wish(request):
    wish_errors = Wish.objects.wish_validator(request.POST)
    print(wish_errors)
    if len(wish_errors) > 0:
        for key, value in wish_errors.items():            
            messages.error(request, value)
        return redirect('/new')
    current_user = User.objects.get(id=request.session['user'])
    new_wish = Wish.objects.create(item=request.POST['item'],description=request.POST['description'],creator=current_user)
    current_user.wishes.add(new_wish)
    return redirect('/wishes')

# READ the BELT REQUIREMENTS AGAIN JONATHAN!!! 
# logout should not allow me to go back after I push back button!!!
def logout(request):
    request.session.flush()
    return redirect('/')

# REMOVE, EDIT, GRANTED button needs to go on the DASHBOARD
def remove(request, id):
    wish = Wish.objects.get(id=id)
    wish.delete()
    return redirect('/wishes')

def edit(request,id):
    context={
        'wishes': Wish.objects.all(),
        'current_user': User.objects.get(id=request.session['user']),
        'edit':Wish.objects.get(id=id)
    }
    return render(request,'edit_wish.html', context)

def granted(request,id):
    granted = Wish.objects.get(id=id)
    granted.granted=True
    granted.save()
    return redirect('/wishes')

# update the wish with VALIDATORS and REDIRECT to dashboard
# Validator = at least 3 characters for item and desc
# route back to dashboard after
def edit_wish(request,id):
    edit = Wish.objects.get(id=id)
    wish_errors = Wish.objects.wish_validator(request.POST)
    print(wish_errors)
    if len(wish_errors) > 0:
        for key, value in wish_errors.items():            
            messages.error(request, value)
        return redirect(f'/edit/{id}')
    edit.item = request.POST['item']
    edit.description = request.POST['description']
    edit.save()
    return redirect('/wishes')



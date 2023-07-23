from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.core import serializers
from django.http import JsonResponse, HttpResponse
from django.http import JsonResponse
import bcrypt
from real_estate_app.models import *

def get(request):
    text = request.GET.get('button_text')
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        if text == "Add to Favorites":
            user = User.objects.get(id= request.session['userid'])
            property = Estate.objects.get(id= int(request.GET.get('id')))
            user.favorites.add(property)
            text = "Remove From Favorites"
            return JsonResponse({'text': text}, status = 200)
        if text == "Remove From Favorites":
            user = User.objects.get(id= request.session['userid'])
            property = Estate.objects.get(id= int(request.GET.get('id')))
            user.favorites.remove(property)
            text = "Add to Favorites"
            return JsonResponse({'text': text}, status = 200)
    return render(request, 'property-single.html')

def sort_properties(request):
    print(request.GET.get('sort_id'))
    if int(request.GET.get('sort_id'))== 0:
        sorted_properties = Estate.objects.all()
    elif int(request.GET.get('sort_id'))== 1:
        sorted_properties = Estate.objects.order_by('-created_at')
    elif int(request.GET.get('sort_id'))== 2:
        sorted_properties = Estate.objects.filter(rent = True)
    elif int(request.GET.get('sort_id'))== 4:
        sorted_properties = Estate.objects.order_by('price')
    elif int(request.GET.get('sort_id'))== 5:
        sorted_properties = Estate.objects.order_by('-price')
    else:
        sorted_properties = Estate.objects.filter(rent = False)
    p = Paginator(sorted_properties, 6)
    page = request.GET.get('page')
    sorted_properties = p.get_page(page)
    sorted_properties_data = []
    for property in sorted_properties:
        # Prepare the property data in a dictionary format
        property_data = {
            'id': property.id,
            'city': property.city,
            'rent': property.rent,
            'currency': property.currency,
            'price': format(property.price, "3,d"),
            'area': property.area,
            'beds': property.beds,
            'baths': property.baths,
            'garages': property.garages,
        }
        sorted_properties_data.append(property_data)
    return JsonResponse(sorted_properties_data, safe=False)


def index(request):
    if "status" in request.session:
        if request.session["status"] == "Logged In":
            context={
            "logged_user": User.objects.get(id= request.session['userid']),
        }
            return render(request, 'index.html', context)
    return render(request, 'index.html')


def properties(request):
    properties = Estate.objects.all()
    p = Paginator(properties, 6)
    page = request.GET.get('page')
    properties = p.get_page(page)
    if "status" in request.session:
        if request.session["status"] == "Logged In":
            context = {
                "logged_user": User.objects.get(id= request.session['userid']),
                "properties": properties
            }
            return render(request, 'property-grid.html', context)
    context = {
            "properties": properties
        }
    return render(request, 'property-grid.html', context)

def properties_new(request):
    if "status" in request.session:
        if request.session["status"] == "Logged In":
            context = {
                "logged_user": User.objects.get(id= request.session['userid']),
            }
                
            return render(request, 'property-new.html', context)
    return redirect('/login_signup')

def properties_single(request, id):
    if "status" in request.session:
        if request.session["status"] == "Logged In":
            user = User.objects.get(id= request.session['userid'])
            favs = user.favorites.all()
            property = Estate.objects.get(id=id)
            isfavorite = False
            for fav in favs:
                if fav == property:
                    isfavorite = True
            context = {
                "logged_user": user,
                "property": property,
                "isfavorite": isfavorite
            }
            return render(request, 'property-single.html', context)
    property = Estate.objects.get(id=id)
    isfavorite = False
    context = {
                "property": property,
                "isfavorite": isfavorite
            }
    return render(request, 'property-single.html', context)

def properties_create(request):
    user = User.objects.get(id= request.session['userid'])
    if request.POST["rent"] == "rent":
        rent = True
    else:
        rent = False
    new_property = Estate(city= request.POST["city"], area= request.POST["area"], beds= request.POST["beds"],
                        baths= request.POST["baths"], garages= request.POST["garages"], stories= request.POST["stories"],
                        currency= request.POST["currency"], price = request.POST["price"], rent = rent, owner = user)
    new_property.save()
    return redirect('/properties')

def properties_edit(request, id):
    if "status" in request.session:
        if request.session["status"] == "Logged In":
            property = Estate.objects.get(id=id)
            user = User.objects.get(id= request.session['userid'])
            if property.owner == user:
                context = {
                    "logged_user": user,
                    "property": property,
                    "cities": ["Ramallah", "Nablus", "Jenin", "Jericho"]
                }
                return render(request, 'property-edit.html', context)
    error = "You cannot edit a property that is not created by you!"
    messages.error(request, error)
    return redirect(f'/properties/{id}')

def properties_update(request, id):
    property = Estate.objects.filter(id=id)
    user = User.objects.get(id= request.session['userid'])
    if property[0].owner == user:
        if request.POST["rent"] == "rent":
            rent = True;
        else:
            rent = False;
        property.update(city= request.POST["city"], area= request.POST["area"], beds= request.POST["beds"],
                        baths= request.POST["baths"], garages= request.POST["garages"], stories= request.POST["stories"],
                        currency= request.POST["currency"], price = request.POST["price"], rent = rent, owner = user)
        messages.success(request,"Updated Succesfully!")
        return redirect(f'/properties/{id}')
    error = "You cannot edit a property that is not created by you!"
    messages.error(request, error)
    return redirect(f'/properties/{id}')

def properties_delete(request, id):
    if "status" in request.session:
        if request.session["status"] == "Logged In":
            user = User.objects.get(id= request.session['userid'])
            property = Estate.objects.get(id= id)
            if user == property.owner:
                property.delete()
                messages.error(request,"Deleted Succesfully!")
                return redirect('/properties')
    error = "You cannot delete a property that is not created by you!"
    messages.error(request, error)
    return redirect(f'/properties/{id}')

def properties_add_fav(request, id):
    user = User.objects.get(id= request.session['userid'])
    property = Estate.objects.get(id= id)
    if request.method == 'GET':
        for fav in user.favorites.all():
            if fav == property:
                return redirect(f'/properties/{id}')
        user.favorites.add(property) 
        return HttpResponse("Success!") # Sending an success response
    user = User.objects.get(id= request.session['userid'])
    property = Estate.objects.get(id= id)
    for fav in user.favorites.all():
        if fav == property:
            return redirect(f'/properties/{id}')
    user.favorites.add(property)
    return redirect(f'/properties/{id}')

def properties_remove_fav(request, id):
    user = User.objects.get(id= request.session['userid'])
    property = Estate.objects.get(id= id)
    user.favorites.remove(property)
    return redirect(f'/properties/{id}')

def properties_fav(request):
    user = User.objects.get(id= request.session['userid'])
    favs = user.favorites.all()
    context = {
        "logged_user": user,
        "favs": favs
    }
    return render(request, 'property-fav.html', context)

def success(request):
    return redirect('/home')

def register(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect ('/login_signup', errors)
    else:
        password = request.POST["pass"]
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        new_user = User(fname= request.POST["fname"], lname= request.POST["lname"], email= request.POST["email"].lower(), phone_number = request.POST["phone_number"], password = pw_hash)
        new_user.save()
        request.session["status"]="Registered"
        messages.success(request,"Register Succesfull!")
        return redirect('/login_signup')
    
def login(request):
    user = User.objects.filter(email=request.POST['email'].lower())
    if user:
        this_user = user[0]
        if bcrypt.checkpw(request.POST['password'].encode() , this_user.password.encode()):
            request.session['userid'] = this_user.id
            request.session["status"] = "Logged In"
            return redirect('/')
    
    messages.error(request,"Please check your Email and Password") 
    return redirect('/login_signup')

def login_signup(request):
    return render(request, 'login_sign.html')


def logout(request):
    request.session.clear()
    return redirect("/")
from django.shortcuts import render, redirect, get_object_or_404
from main.forms import ProductForm
from main.models import Product
from django.http import HttpResponse, HttpResponseRedirect
from django.core import serializers
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import datetime
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils.html import strip_tags
import json

@login_required(login_url='/login')
def show_main(request):
    filter_type = request.GET.get("filter", "all") 

    if filter_type == "all":
        product_list = Product.objects.all()
    else:
        product_list = Product.objects.filter(user=request.user)


    context = {
        'npm': '2406396590',
        'name': request.user.username,
        'class': 'PBP B',
        'product_list': product_list,
        'last_login': request.COOKIES.get('last_login', 'Never')
    }
    return render(request, "main.html",context)

@login_required(login_url='/login')
def create_product(request):
    form = ProductForm(request.POST or None)

    if form.is_valid() and request.method == 'POST':
        product_entry = form.save(commit = False)
        product_entry.user = request.user
        product_entry.save()
        return redirect('main:show_main')

    context = {'form': form}
    return render(request, "create_product.html", context)

@login_required(login_url='/login')
def show_product(request, name):
    product = get_object_or_404(Product, name=name)

    context = {
        'product': product
    }

    return render(request, "product_detail.html", context)

def show_xml(request):
     product_list = Product.objects.all()
     xml_data = serializers.serialize("xml", product_list)
     return HttpResponse(xml_data, content_type="application/xml")



def show_json(request):
    product_list = Product.objects.select_related('user').all()
    data = [
        {
            'name': product.name,
            'description': product.description,
            'price' : product.price,
            'category': product.category,
            'thumbnail': product.thumbnail,
            'created_at': product.created_at.isoformat() if product.created_at else None,
            'is_featured': product.is_featured,
            'user_id': product.user_id,
            'username': product.user.username if product.user else 'Anonymous'
        }
        for product in product_list
    ]

    return JsonResponse(data, safe=False)

def show_xml_by_name(request, product_name):
    try:
        product_item = Product.objects.filter(name=product_name)
        xml_data = serializers.serialize("xml", product_item)
        return HttpResponse(xml_data, content_type="application/xml")
    except Product.DoesNotExist:
        return HttpResponse(status=404)

    
def show_json_by_name(request, product_name):
    try:
        product = Product.objects.select_related('user').get(name=product_name)
        data = {
            'name': product.name,
            'description': product.description,
            'price' : product.price,
            'category': product.category,
            'thumbnail': product.thumbnail,
            'created_at': product.created_at.isoformat() if product.created_at else None,
            'is_featured': product.is_featured,
            'user_id': product.user_id,
        }
        return JsonResponse(data)
    except Product.DoesNotExist:
        return JsonResponse({'detail': 'Not found'}, status=404)
    
def register(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been successfully created!')
            return redirect('main:login')
    context = {'form':form}
    return render(request, 'register.html', context)

def login_user(request):
   if request.method == 'POST':
      form = AuthenticationForm(data=request.POST)

      if form.is_valid():
        user = form.get_user()
        login(request, user)
        response = HttpResponseRedirect(reverse("main:show_main"))
        response.set_cookie('last_login', str(datetime.datetime.now()))
        return response

   else:
      form = AuthenticationForm(request)
   context = {'form': form}
   return render(request, 'login.html', context)

def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('main:login'))
    response.delete_cookie('last_login')
    return response

def clear_products(request):
    Product.objects.all().delete()
    return redirect("main:show_main")

def edit_product(request, product_name):
    products = get_object_or_404(Product, name=product_name)
    form = ProductForm(request.POST or None, instance=products)
    if form.is_valid() and request.method == 'POST':
        form.save()
        return redirect('main:show_main')

    context = {
        'form': form
    }

    return render(request, "edit_product.html", context)

def delete_product(request, product_name):
    product = get_object_or_404(Product, name=product_name)
    product.delete()
    return HttpResponseRedirect(reverse('main:show_main'))

@csrf_exempt
@require_POST
def add_product_entry_ajax(request):
    name = strip_tags(request.POST.get("name"))
    price = request.POST.get("price")
    description = strip_tags(request.POST.get("description"))
    category = request.POST.get("category")
    thumbnail = request.POST.get("thumbnail")
    is_featured = request.POST.get("is_featured") == 'on'
    user = request.user

    new_product = Product(
        name=name,
        price=int(price),
        description=description,
        category=category,
        thumbnail=thumbnail,
        is_featured=is_featured,
        user=user
    )
    new_product.save()

    return HttpResponse(b"CREATED", status=201)

@csrf_exempt
@require_POST
def edit_product_ajax(request, product_name):
    try:
        product = Product.objects.get(name=product_name)
        
        if product.user != request.user:
            return JsonResponse({'status': 'error', 'message': 'Unauthorized'}, status=403)

        product.name = request.POST.get("name", product.name)
        product.price = int(request.POST.get("price", product.price))
        product.description = request.POST.get("description", product.description)
        product.category = request.POST.get("category", product.category)
        product.thumbnail = request.POST.get("thumbnail", product.thumbnail)
        product.is_featured = request.POST.get("is_featured") == 'on'
        
        product.save()
        
        return JsonResponse({'status': 'success', 'message': 'Product updated successfully'})
    except Product.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Product not found'}, status=404)
    
@csrf_exempt
@require_POST
def delete_product_ajax(request, product_name):
    try:
        product = Product.objects.get(name=product_name, user=request.user)
        product.delete()
        return JsonResponse({'status': 'success', 'message': 'Product deleted'})
    except Product.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Product not found or unauthorized'}, status=404)
    
@csrf_exempt
def register_ajax(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'status': 'success', 'message': 'Registration successful! Please log in.'})
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors.get_json_data()}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)


@csrf_exempt
def login_ajax(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            response_data = {'status': 'success', 'message': 'Login successful!'}
            response = JsonResponse(response_data)
            response.set_cookie('last_login', str(datetime.datetime.now()))
            return response
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors.get_json_data()}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)
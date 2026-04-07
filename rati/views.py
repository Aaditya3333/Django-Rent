import re
from django.shortcuts import render,redirect,get_object_or_404
from .models import Rent,Profile,Product,Contact
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.contrib import messages
from .form import ProfileForm,ProductForm,ProductSearchForm
from django.contrib.auth.forms import PasswordChangeForm
from django.core.mail import send_mail
from django.db.models import Q
# Create your views here.
def index(request):
    rent=Product.objects.filter(isdelete=True)
    paginator=Paginator(rent,3)
    p_num=request.GET.get('page')
    data=paginator.get_page(p_num)
    total=data.paginator.num_pages
    if request.method=='POST':
        name=request.POST['name']
        email=request.POST['email']
        phone=request.POST['phone']
        message=request.POST['message']
        user=Contact(name=name,email=email,phone=phone,message=message)
        user.save()
        messages.success(request,'Thank you for contacting us')
        return redirect('index')
    context={
        'rent':data,
        'num':[ i+1 for i in range(total)]
    }
    return render(request,'rati/index.html',context)

def about(request):
    return render(request,'rati/about.html')

def contact(request):
    if request.method=='POST':
        name=request.POST['name']
        email=request.POST['email']
        phone=request.POST['phone']
        message=request.POST['message']
        user=Contact(name=name,email=email,phone=phone,message=message)
        user.save()
        subject='Connect with us'
        message="Thank you for your message/feedback.Your review means a lot"
        from_email='aadityapoudel68@gmail.com'
        recipient_list=[email]
        
        send_mail(subject,message,from_email,recipient_list,fail_silently=False)
        messages.success(request,'Thank you for contacting us.')
        return redirect('contact')
    return render(request,'rati/contact.html')

def rents(request):
    rent=Product.objects.filter(isdelete=True)
    context={
        'rent':rent
    }
    return render(request,'rati/rents.html',context)

def blogs(request):
    return render(request,'rati/blogs.html')

def privacy(request):
    return render(request,'rati/privacypolicy.html')

def support(request):
    return render(request,'rati/support.html')

@login_required(login_url='login')
def profile(request):
    return render(request,'profile/profile.html')

@login_required(login_url='login')
def update_profile(request):
    profile,created=Profile.objects.get_or_create(user=request.user)
    form=ProfileForm(instance=profile)
    if request.method == 'POST':
        form=ProfileForm(request.POST,request.FILES,instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    context={
        'form':form
    }
    return render(request,'profile/update_profile.html',context)

@login_required(login_url='login')
def upload_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user
            product.save()
            return redirect('index')  
    else:
        form = ProductForm()
    return render(request, 'rati/upload_product.html', {'form': form})


@login_required(login_url='login')
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id, seller=request.user)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('index')  # or any other page
    else:
        form = ProductForm(instance=product)

    return render(request, 'rati/edit_product.html', {'form': form})

@login_required
def soft_delete_property(request, pk):
    product = get_object_or_404(Product, pk=pk, seller=request.user)
    product.isdelete = False
    product.save()
    return redirect('index')

def product_search(request):
    # Get all unique locations for the dropdown
    existing_locations = Product.objects.filter(isdelete=True) \
        .exclude(location__isnull=True) \
        .exclude(location__exact='') \
        .values_list('location', flat=True) \
        .distinct()

    products = Product.objects.filter(isdelete=True)

    # Get filter parameters from request
    location = request.GET.get('location')
    categories = request.GET.getlist('categories')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    # Apply filters
    if location:
        products = products.filter(location__icontains=location)

    if categories:
        products = products.filter(categories__name__in=categories).distinct()

    if min_price:
        products = products.filter(price__gte=min_price)

    if max_price:
        products = products.filter(price__lte=max_price)

    # Pagination
    paginator=Paginator(products,3)
    p_num=request.GET.get('page')
    data=paginator.get_page(p_num)
    total=data.paginator.num_pages

    # Build query string without 'page'
    querydict = request.GET.copy()
    querydict.pop('page', None)
    query_string = querydict.urlencode()

    context = {
        
        'existing_locations': existing_locations,
        'selected_location': location,
        'selected_categories': categories,
        'min_price': min_price or '20000',
        'max_price': max_price or '25000',
        'query_string': query_string,
        'products':data,
        'num':[ i+1 for i in range(total)]
    }
    return render(request, 'products/search.html', context)




'''
########################################################################
########################################################################
                          AUTH PART
########################################################################
########################################################################                          

'''

def log_in(request):
    if request.method == 'POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        if not User.objects.filter(username=username).exists():
            messages.error(request,"Username is not valid")
            return redirect('login')
        user=authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            remember_me=request.POST.get("remember_me")
            if remember_me:
                request.session.set_expiry(12000)
            else:
                request.session.set_expiry(0)
            return redirect('index')
    return render(request,'auth/login.html')

def register(request):
    if request.method == 'POST':
        fname=request.POST['fname']
        lname=request.POST['lname']
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        password1=request.POST['password1']

        if password == password1:
            try:
                validate_password(password)
                error=[]
                if User.objects.filter(username=username).exists():
                    error.append("Username already exists")

                if User.objects.filter(email=email).exists():
                    error.append("This email is already registered")
                    return redirect('register')
                
                if not re.search(r'[A-Z]',password):
                    error.append("Your password must have one upper letter")

                if not re.search(r'\d',password):
                    error.append("Your password must have one numeric deigit")
                
                if error:
                    for i in error:
                        messages.error(request,i)
                    return redirect('register')
                
                else:
                    User.objects.create_user(first_name=fname,last_name=lname,username=username,email=email,password=password)
                    messages.success(request,'Registration Successful,Please login')
                    return redirect('register')
            except ValidationError as e:
                for error in e.messages:
                    messages.error(request,error)
                return redirect('register')
        else:
            messages.error(request,'Password and confirm password doesnot match')
            return redirect('register')
    return render(request,'auth/register.html')

def log_out(request):
    logout (request)
    return redirect('login')

def change_password(request):
    form=PasswordChangeForm(user=request.user)
    if request.method == 'POST':
        form=PasswordChangeForm(user=request.user,data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('log_in')


    return render(request,'auth/change_password.html',{'form':form})

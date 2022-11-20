
# Imports needed for the project
from django.shortcuts import render, redirect
from django.contrib.auth.models import Group
from clothingstore.decorators import admin_only, allowed_users
from clothingstore.decorators import unauthenticated_user
from django.http import HttpResponse
from .models import Customer, Order, Product, Reviews
from .forms import UserForm, CustomerForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .filters import ProductFilter
from django.core.paginator import Paginator
from django.core.files.storage import FileSystemStorage

# Create your views here.


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def home(request):  
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'clothingstore/home.html', context)


@unauthenticated_user
def login_home(request):
    if request.method == 'POST':
        print(request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        
        if user is not None:
            print('Authenticated')
            login(request, user)
            return redirect("home")
        else:
            msg = 'Email or Password is incorrect'
            messages.add_message(request, messages.INFO, msg)
            # print('not authenticated')
            return redirect("login")
    return render(request, 'clothingstore/login.html')


def logout_home(request):
    logout(request)
    return redirect('login')


@unauthenticated_user
def signup_home(request):

    form = UserForm()
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid:
            try:
                user_check = Customer.objects.get(user__username=request.POST.get('username')) # noqa
            except Customer.DoesNotExist:
                user_check = None
            if user_check:
                msg = f"username {user_check} has been taken!!"
                messages.info(request, msg)
            else:  
                user = form.save()
                Customer.objects.create(user=user, first_name=form.cleaned_data['first_name'], last_name=form.cleaned_data['last_name'], id_number=form.cleaned_data['id_number']) # noqa
                group = Group.objects.get(name='customer')
                user.groups.add(group) 
                msg = f"{form.cleaned_data['username']} has been registered"
                messages.add_message(request, messages.SUCCESS, msg)
                return redirect("login")

    context = {'form': form}
    return render(request, 'clothingstore/signup.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def product(request, pk):
    product_detail = Product.objects.get(id=pk)
    form = Reviews()
    # __ underscore is used for dealing
    #  with another model class .
    customerobj = Customer.objects.get(user__username=request.user.username)
    customer = Customer.objects.get(id=(request.user.id)-1)
    # getting this data to javascript <script> <tag>  
    details = {'quantity': product_detail.product_quantity, 'id': product_detail.id} # noqa
    # print(request.POST)
    # this data to be on html template
    
    if (request.method == 'POST' and request.POST['action'] == 'orderData'):
        # PRODUCT_DATA
        # print('Product Data')
        # print('Product Quantity ', request.POST.get('productQuantity'))
        
        if int(request.POST.get('productQuantity')) != 0:      
            productprice = request.POST.get('productprice').split('$')[0]
            productName = request.POST.get('productName')
            # productsize = request.POST.get('productsize')
            # productreview = request.POST.get('productReview')
            productquantity = request.POST.get('productQuantity')
            product_detail.product_quantity = product_detail.product_quantity - int(productquantity) # noqa
            product_detail.save(update_fields=['product_quantity'])
        
            # adding the order in order to work with many to many relationship 
            # it is necessary to make an object and then 
            # using the set method to add other details 
            instance = Order.objects.create(customer=customerobj, product_quantity=productquantity, product_price=productprice) # noqa
            productobj = Product.objects.filter(product_name=productName)
            instance.product.set(productobj) 
            
        else: 
            # print('Product is out of stock ')
            messages.info(request, 'Product is out of stock')

    elif request.method == 'POST' and request.POST['action'] == 'modalData':
        # Modal Data 
        print(' Modal Data')
        print(request.POST)
        phonenumber = request.POST.get('phonenumber')
        address = request.POST.get('address')
        # print(f"Phone Number :", phonenumber)
        # print( f"Address:",address)
        customer.phonenumber = phonenumber
        customer.address = address 
        customer.save(update_fields=['phonenumber', "address"])      
        # print('After saving -- Result ')
        # print(customer.phonenumber)
        # print(customer.address)

    # Review_portion where user can give review on a product
    elif request.method == 'POST' and request.POST['action'] == 'review':
        # print('In Review Session!!')   
        # print(request.POST.get('text-val')) 
        if request.POST.get('text-val'):
            # print('Success Review is not Empty')
            customer_name = Customer.objects.get(user__id=request.user.id)
            # print('Customer:', customer_name)
            # Customer should be able to review only once
            review_check_for_product = Reviews.objects.filter(customer_name=customer_name, product__id=product_detail.id) # noqa
            # print('Customer Reviews', review_check_for_product)
            if len(review_check_for_product) >= 1:
                messages.info(request, "You have already given a Review.") 
            else:
                review_text = request.POST.get('text-val')
                # print('Review:', review_text) 
                instance = Reviews.objects.create(customer_name=customer_name, review_text=review_text) # noqa
                product_name = Product.objects.filter(id=product_detail.id)
                instance.product.set(product_name)  
                # print('Form is valid!!')
        else:
            msg = "Please give the Correct Review"
            messages.add_message(request, messages.INFO, msg)
    
    all_reviews = Reviews.objects.filter(product__id=product_detail.id)   
    # print('All_Reviews', all_reviews)
    context = {'product_detail': product_detail, 'details': details, 'customer': customer, 'form': form, 'reviews': all_reviews} # noqa
    return render(request, 'clothingstore/product.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def CustomerProfile(request, pk):
    form = CustomerForm()
    user = Customer.objects.get(id=(pk-1))
    if request.method == 'POST':
        # print(request.POST)
        file = request.FILES.get("file")
        # print('file name',file.name)
        # print('file object',file)
        fs = FileSystemStorage()
        filename = fs.save(file.name, file)
        # print(filename)
        user.profilepic = filename
        user.save() 
        form = CustomerForm(request.POST)
        if form.is_valid():
            # UPDATING_CUSTOMER_PROFILE
            user.user.username = request.POST.get('username')
            user.first_name = request.POST.get('firstname')
            user.last_name = request.POST.get('lastname')
            user.user.email = request.POST.get('email')
            user.id_number = request.POST.get('idnumber')    
            # user.profilepic = request.FILES.get('file')
            print(request.POST)
            print('here')
            print(request.FILES.get('file'))
            user.save(update_fields=['first_name', 'last_name', 'id_number'])
            user.user.save(update_fields=['email', 'username'])
            msg = f'{user.user.username} updated successfully!!!'
            messages.success(request, msg)
            return redirect('customerProfile', pk=pk)
    # using serializers approach to pass queryset  to the javascript
    orders = Order.objects.all()
    print(user.profilepic.url)
    context = {'form': form, 'user': user, 'orders': orders}
    return render(request, 'clothingstore/customer.html', context)    


def deleteCustomerOrder(request):
    if request.method == 'POST':
        order = Order.objects.get(id=request.POST.get('orderid'))
        Order.delete(order) 
    return render(request, 'clothingstore/customer.html')


@login_required(login_url='login')
def products(request):
    all_products = Product.objects.all()
    product_listing = ProductFilter(request.GET, all_products)
    paginator = Paginator(product_listing.qs, 4)
    # print(paginator.count)
    # print(paginator.num_pages)
    page_number = request.GET.get('page')
    productsFinalListing = paginator.get_page(page_number)
    # print(productsFinalListing)
    context = {'product_listing': product_listing, 'productsFinalListing': productsFinalListing, 'num_of_products': range(1, paginator.num_pages+1)} # noQA
    return render(request, 'clothingstore/products.html', context)


@login_required(login_url='login')
@admin_only
def dashboard(request):
    return HttpResponse("This is page!!")
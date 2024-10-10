
from django.http import HttpResponseNotFound, JsonResponse
from django.shortcuts import render, redirect,  get_object_or_404
from django.views import View
from .models import Customer, Product, Reservation, Feedback, Cart, OrderPlaced, Payment  # Replace with your actual model
from .forms import ReservationForm, CustomerProfileForm,  BlogForm  # Ensure you have a form defined
from decimal import Decimal
from django.db.models import Count, Q, F
from django.contrib import messages
from . forms import CustomerRegistrationForm, CustomerProfileForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import BlogPost
import stripe
from django.conf import settings
# Create your views here.
def home(request):
    return render(request,"app/home.html")


class aboutview(View):
    def get(self,request):
        return render(request,"app/about.html")
    
class cartview(View):
    def get(self,request):
        return render(request,"app/cart.html")

class wishlistview(View):
    def get(self,request):
        return render(request,"app/wishlist.html")
    
class contactview(View):
    def get(self,request):
        return render(request,"app/contact.html")
    
class homeview(View):
    def get(self,request):
        return render(request,"app/home.html")
    
# @method_decorator(login_required,name='dispatch')    
class ProfileView(View):
    def get(self,request):
        form = CustomerProfileForm()
        return render(request, 'app/profile.html',locals())
    def post(self,request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            village = form.cleaned_data['village']
            city = form.cleaned_data['city']
            mobile = form.cleaned_data['mobile']
            state = form.cleaned_data['state']
            pincode = form.cleaned_data['pincode']

            reg = Customer(user=user,name=name,village=village,city=city,mobile=mobile,state=state,pincode=pincode)
            reg.save()
            messages.success(request, "Congratulations! Profile Saved Successfully")
        else:
            messages.warning(request,"Invalid Input Data")
        return render(request, 'app/profile.html',locals())


class blogview(View):
    def get(self,request):
        return render(request,"app/blog.html")

class shopview(View):
    def get(self,request):
        return render(request,"app/shop.html")
    
def feedback(request):
    return render(request, 'app/feedback.html')

class reservation_view(View):
    def get(self, request):
        form = ReservationForm()
        return render(request, 'app/reservation_form.html', locals())

    def post(self, request):
        form = ReservationForm(request.POST)
        if form.is_valid():
            # Set the user for the reservation
            reservation = form.save(commit=False)
            reservation.user = request.user  # assuming the user is logged in
            reservation.save()
            messages.success(request, "Congratulations! Table Booked Successfully")
            return redirect('success')  # Change this to your URL name for managing reservations
        else:
            messages.warning(request, "Invalid Input Data")
        return render(request, 'app/reservation_form.html', {'form': form})

    
# def reservation_view(request):
#     if request.method=="POST":
#         reservation=Reservation()
#         name=request.POST.get('name')
#         email=request.POST.get('email')
#         message=request.POST.get('message')
#         date=request.POST.get('date')
#         time=request.POST.get('time')
#         guests=request.POST.get('guests')
#         # data, time, guests
#         reservation.name=name
#         reservation.email=email
#         reservation.message=message
#         reservation.date=date
#         reservation.time=time
#         reservation.guests=guests
#         reservation.save()
#         # return HttpResponse("<center><h1>THANKS FOR YOUR FEEDBACK</h1><center>")
#         return redirect("/success")
#     return render(request, 'app/reservation_form.html',locals())

def success_view(request):
    return render(request, 'app/success.html')

def search(request):
    query = request.GET.get('search')
    # Check if the query is a valid decimal for price
    try:
        price = Decimal(query)
        products = Product.objects.filter(
            Q(food_name__icontains=query) |
            Q(food_category__icontains=query) |
            Q(sub_category__icontains=query) |
            Q(price__lte=query)  # Exact match for price
        )
    except:
        # If the query is not a valid decimal, filter without price
        products = Product.objects.filter(
            Q(food_name__icontains=query) |
            Q(food_category__icontains=query) |
            Q(sub_category__icontains=query)
        )

    return render(request, "app/search.html", {'products': products, 'query': query})

def feedback(request):
    if request.method=="POST":
        feedback=Feedback()
        name=request.POST.get('name')
        email=request.POST.get('email')
        comment=request.POST.get('comment')
        feedback.name=name
        feedback.email=email
        feedback.comment=comment
        feedback.save()
        # return HttpResponse("<center><h1>THANKS FOR YOUR FEEDBACK</h1><center>")
        return redirect("/")
    return render(request, 'app/feedback.html',locals())

class ProductDetail(View):
    def get(self, request, pk):
        try:
            # Fetch the product from the database using the provided primary key (pk)
            product = Product.objects.get(id=pk)
            
            # Fetch the wishlist items for the current user and the specific product
            # wishlist = Wishlist.objects.filter(Q(product=product) & Q(user=request.user))
            
            # # Get recommendations for the current product
            # recommendations = recommend(product.food_name)
            
            # # Get same category recommendations for the current product
            # same_category_recommendations = same_recommend1(product.food_name)

            context = {
                'product': product,
                # 'wishlist': wishlist,
                # 'recommendations': recommendations,
                # 'same_category_recommendations': same_category_recommendations,
            }
            return render(request, 'app/productdetail.html', context)
        except Product.DoesNotExist:
            # Handle the case where the product with the given primary key doesn't exist
            return HttpResponseNotFound("The requested product does not exist.")

class CustomerRegistrationView(View):
    def get(self,request):
        form = CustomerRegistrationForm()
        return render(request, 'app/customerregistration.html',locals())
    def post(self,request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Congratulations! User Register Successfully")
        else:
            messages.warning(request,"Inavalid Input Data")
        return render(request, 'app/customerregistration.html',locals())

@method_decorator(login_required,name='dispatch')    
class ProfileView(View):
    def get(self,request):
        form = CustomerProfileForm()
        return render(request, 'app/profile.html',locals())
    def post(self,request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            village = form.cleaned_data['village']
            city = form.cleaned_data['city']
            mobile = form.cleaned_data['mobile']
            state = form.cleaned_data['state']
            pincode = form.cleaned_data['pincode']

            reg = Customer(user=user,name=name,village=village,city=city,mobile=mobile,state=state,pincode=pincode)
            reg.save()
            messages.success(request, "Congratulations! Profile Saved Successfully")
        else:
            messages.warning(request,"Invalid Input Data")
        return render(request, 'app/profile.html',locals())

@login_required    
def address(request):
    add = Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html',locals())
class updateAddress(View):
    def get(self,request,pk):
        add = Customer.objects.get(pk=pk)
        form = CustomerProfileForm(instance=add)
        return render(request, 'app/updateAddress.html',locals())
    def post(self,request,pk):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            add = Customer.objects.get(pk=pk)
            add.name = form.cleaned_data['name']
            add.village = form.cleaned_data['village']
            add.city = form.cleaned_data['city']
            add.mobile = form.cleaned_data['mobile']
            add.state = form.cleaned_data['state']
            add.pincode = form.cleaned_data['pincode']
            add.save()
            messages.success(request,"Congratulations! Profile Updated Successfully")
        else:
            messages.warning(request,"Invalid Input Data")
        return redirect("address")
     
class ManageReservationView(View):
    def get(self, request):
        reservations = Reservation.objects.filter(user=request.user)
        return render(request, 'app/managereservation.html', {'reservations': reservations})

class DeleteReservationView(View):
    def get(self, request, reservation_id):
        # Get the reservation object, or return 404 if not found
        reservation = get_object_or_404(Reservation, id=reservation_id, user=request.user)

        # Check if the reservation belongs to the current user
        if reservation.user == request.user:
            reservation.delete()
            messages.success(request, "Reservation deleted successfully.")
        else:
            messages.error(request, "You are not authorized to delete this reservation.")

        return redirect("manage_reservation")  # Redirect back to manage reservations page
    
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get("prod_id")
    product = Product.objects.get(id=product_id)
    
    # Check if the product is already in the cart for the current user
    existing_cart_item = Cart.objects.filter(user=user, product=product).first()
    if existing_cart_item:
        # If the product already exists in the cart, increase the quantity by 1
        existing_cart_item.quantity = F('quantity') + 1
        existing_cart_item.save()
        # messages.success(request, "Quantity updated successfully.")
    else:
        # If the product is not in the cart, add it to the cart with quantity 1
        Cart.objects.create(user=user, product=product)
        # messages.success(request, "Product added to cart successfully.")
    
    return redirect("/cart")

def show_cart(request):
    user = request.user
    cart_items = Cart.objects.filter(user=user)
    
    total_amount = 0
    for cart_item in cart_items:
        value = cart_item.quantity * cart_item.product.price
        total_amount += value
    
    
    return render(request, 'app/addtocart.html', {'cart_items': cart_items, 'total_amount': total_amount})


stripe.api_key = settings.STRIPE_SECRET_KEY  # Set your Stripe secret key

@method_decorator(login_required, name='dispatch')
class Checkout(View):
    def get(self, request):
        user = request.user
        add = Customer.objects.filter(user=user)
        cart_items = Cart.objects.filter(user=user)

        # Calculate total amount
        totalamount = sum(item.quantity * item.product.price for item in cart_items)

        # Create a Stripe Payment Intent
        payment_intent = stripe.PaymentIntent.create(
            amount=int(totalamount * 100),  # Amount in cents
            currency='usd',  # Change to your desired currency
            payment_method_types=["card"],
        )

        # Save payment details
        payment = Payment(
            user=user,
            amount=totalamount,
            stripe_payment_intent_id=payment_intent.id,
            stripe_payment_status=payment_intent.status,
            paid=False
        )
        payment.save()

        return render(request, 'app/checkout.html', {
            'add': add,
            'cart_items': cart_items,
            'totalamount': totalamount,
            'client_secret': payment_intent['client_secret'],  # Pass client secret to template
        })
@login_required
def payment_done(request):
    # Use payment intent ID to find the payment
    payment_intent_id = request.GET.get('payment_intent')  # Assuming you pass this in the query params
    user = request.user
    
    # Fetch the payment associated with the payment intent
    payment = Payment.objects.get(stripe_payment_intent_id=payment_intent_id)
    payment.paid = True
    payment.stripe_payment_status = 'succeeded'  # Assuming payment was successful
    payment.save()

    # Get the customer's selected address
    cust_id = request.GET.get('cust_id')  # Ensure you pass cust_id in the request
    customer = Customer.objects.get(id=cust_id)

    # Save order details
    cart = Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(
            user=user,
            customer=customer,
            product=c.product,
            quantity=c.quantity,
            payment=payment
        ).save()
        c.delete()  # Remove items from the cart after successful payment

    return redirect("orders")  # Redirect to orders page
@login_required
def orders(request):
    order_placed=OrderPlaced.objects.filter(user=request.user)
    return render(request, 'app/orders.html',locals())


def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')
        product = get_object_or_404(Product, id=prod_id)
        cart_item, created = Cart.objects.get_or_create(product=product, user=request.user)
        cart_item.quantity += 1
        cart_item.save()
        cart = Cart.objects.filter(user=request.user)
        amount = sum(p.quantity * p.product.price for p in cart)
        totalamount = amount

        data = {
            'quantity': cart_item.quantity,
            'amount': amount,
            'totalamount': totalamount
        }
        return JsonResponse(data)


def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')
        product = get_object_or_404(Product, id=int(prod_id))
        cart_item = get_object_or_404(Cart, product=product, user=request.user)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        cart = Cart.objects.filter(user=request.user)
        amount = sum(p.quantity * p.product.price for p in cart)
        totalamount = amount

        data = {
            'quantity': cart_item.quantity,
            'amount': amount,
            'totalamount': totalamount
        }
        return JsonResponse(data)


def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')
        
        # Use get_object_or_404 to retrieve the cart item
        cart_item = get_object_or_404(Cart, product_id=prod_id, user=request.user)
        # Delete the cart item
        cart_item.delete()

        # Recalculate the amount and total amount after removing the item
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = sum(p.quantity * p.product.price for p in cart)
        totalamount = amount 

        # Prepare data to send back in the JSON response
        data = {
            'amount': amount,
            'totalamount': totalamount
        }
        return JsonResponse(data)
def create_blog(request):
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)  # Handle file upload
        if form.is_valid():
            form.save()  # Save the new blog post
            return redirect('blog')  # Redirect to a page that lists blogs
    else:
        form = BlogForm()
    return render(request, 'app/create_blog.html', {'form': form})

def blog(request):
    blog_posts = BlogPost.objects.all()  # Get all blog posts
    return render(request, 'app/blog.html', {'blog_posts': blog_posts})

class paysuccessView(View):
    def get(self, request):
        return render(request, 'app/paysuccess.html')

class CancelView(View):
    def get(self, request):
        return render(request, 'app/cancel.html')


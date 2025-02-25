from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Cart, Order
from .forms import CartForm,ProductForm,EmailChangeForm,EditProfileForm, ChangePasswordForm
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth import logout,update_session_auth_hash
from django import forms
from django.contrib import messages
from django.contrib.auth.models import User

def product_list(request):
    products = Product.objects.all()  # Capitalized 'Product'
    return render(request, 'store/product_list.html', {'products': products})

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)  # Capitalized 'Product'
    return render(request, 'store/product_detail.html', {'product': product})

def add_to_cart(request, product_id):
    if not request.user.is_authenticated:
        return redirect('login')  # Redirect anonymous users to login page

    product = get_object_or_404(Product, id=product_id)
    cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)

    if not created:
        cart_item.quantity += 1
    cart_item.save()
    return redirect('cart')

@login_required
def cart_view(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, 'store/cart.html', {'cart_items': cart_items, 'total_price': total_price})

@login_required
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_detail', product_id=product.id)
    else:
        form = ProductForm(instance=product)

    return render(request, 'store/edit_product.html', {'form': form, 'product': product})
def checkout(request):
    cart_items = Cart.objects.filter(user=request.user)
    
    if not cart_items:  # If cart is empty, prevent checkout
        return redirect('cart')

    total_price = sum(item.product.price * item.quantity for item in cart_items)

    if request.method == "POST":
        order = Order.objects.create(user=request.user, total_price=total_price)

        # Move cart items to order (optional - depends on your needs)
        for item in cart_items:
            item.delete()  # Clear the cart after checkout

        return redirect('order_success')

    return render(request, 'store/checkout.html', {'cart_items': cart_items, 'total_price': total_price})

def order_success(request):
    return render(request, 'store/order_success.html')


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    confirm_email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "confirm_email", "password1", "password2")

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        confirm_email = cleaned_data.get("confirm_email")

        if email != confirm_email:
            raise forms.ValidationError("Emails do not match")

        return cleaned_data

def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to login after signup
    else:
        form = CustomUserCreationForm()
    return render(request, 'store/signup.html', {'form': form})

@login_required
def profile_view(request):
    return render(request, 'store/profile.html', {'user': request.user})

@staff_member_required
@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('product_list')  # Redirect to product list after adding
    else:
        form = ProductForm()

    return render(request, 'store/add_product.html', {'form': form})   
 
@login_required
def change_email(request):
    if request.method == "POST":
        form = EmailChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirect to the profile page after email update
    else:
        form = EmailChangeForm(instance=request.user)
    
    return render(request, 'store/change_email.html', {'form': form})


def update_cart(request, cart_item_id):
    cart_item = get_object_or_404(Cart, id=cart_item_id, user=request.user)

    if request.method == "POST":
        new_quantity = request.POST.get("quantity")
        if new_quantity and int(new_quantity) > 0:
            cart_item.quantity = int(new_quantity)
            cart_item.save()
        else:
            cart_item.delete()  # If the quantity is 0, remove the item from the cart

    return redirect('cart')  # Redirect back to cart page

def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(Cart, id=cart_item_id, user=request.user)
    cart_item.delete()
    return redirect('cart')  # Redirect back to cart page


@login_required
def profile(request):
    password_form = ChangePasswordForm()

    if request.method == 'POST':
        if 'change_password' in request.POST:
            password_form = ChangePasswordForm(request.POST)
            if password_form.is_valid():
                if request.user.check_password(password_form.cleaned_data['current_password']):
                    request.user.set_password(password_form.cleaned_data['new_password'])
                    request.user.save()
                    update_session_auth_hash(request, request.user)  # Keep user logged in
                    messages.success(request, "Password changed successfully!")
                    return redirect('profile')
                else:
                    messages.error(request, "Current password is incorrect.")

    return render(request, 'store/profile.html', {'password_form': password_form})


@login_required
def edit_profile(request):
    form = EditProfileForm(instance=request.user)

    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('profile')

    return render(request, 'store/edit_profile.html', {'form': form})


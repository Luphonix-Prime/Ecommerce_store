from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Cart, Order, Category
from .forms import CartForm, ProductForm, EmailChangeForm, EditProfileForm, ChangePasswordForm, CategoryForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth import logout,update_session_auth_hash
from django import forms
from django.contrib import messages
from django.utils.timezone import now
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView

from datetime import datetime, timedelta
from django.db.models import Sum, Count
class CustomLoginView(LoginView):
    template_name = 'store/login.html'  # Use your custom login template

    def get_success_url(self):
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return '/dashboard'  # Redirect admins and staff to the dashboard
        return '/products'  # Redirect normal users to the product list

# def product_list(request):
#     products = Product.objects.all()  # Capitalized 'Product'
#     return render(request, 'store/product_list.html', {'products': products})

# def product_detail(request, product_id):
#     product = get_object_or_404(Product, id=product_id)  # Capitalized 'Product'
#     return render(request, 'store/product_detail.html', {'product': product})

def add_to_cart(request, product_id):
    if not request.user.is_authenticated:
        return redirect('login')  # Redirect anonymous users to login page

    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))  # Get quantity from form, default to 1

    cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)

    if not created:
        cart_item.quantity += quantity  # Increase quantity if already exists
    else:
        cart_item.quantity = quantity

    cart_item.save()
    messages.success(request, f"{quantity}x {product.name} added to cart!")  # Show success message
    return redirect('cart')

@login_required
def cart_view(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, 'store/cart.html', {'cart_items': cart_items, 'total_price': total_price})

# @login_required
# def edit_product(request, product_id):
#     product = get_object_or_404(Product, id=product_id)

#     if request.method == "POST":
#         form = ProductForm(request.POST, request.FILES, instance=product)
#         if form.is_valid():
#             form.save()
#             return redirect('product_detail', product_id=product.id)
#     else:
#         form = ProductForm(instance=product)

#     return render(request, 'store/edit_product.html', {'form': form, 'product': product})
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



def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    categories = Category.objects.all()

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('store/product_detail', product_id=product.id)
    else:
        form = ProductForm(instance=product)

    return render(request, 'store/edit_product.html', {'form': form, 'product': product, 'categories': categories})

@login_required
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    return redirect('product_list')  # Redirect to product list after deleting

def product_list(request):
    products = Product.objects.select_related('category').all()
    categories = Category.objects.prefetch_related('products').all()  # Use 'products' instead of 'product_set'
    return render(request, 'store/product_list.html', {'products': products, 'categories': categories})



def product_detail(request, product_id):
    product = get_object_or_404(Product.objects.select_related('category'), id=product_id)
    return render(request, 'store/product_detail.html', {'product': product})


# List Categories
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'store/categories.html', {'categories': categories})

# Add Category
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('categories')  # Make sure this URL name exists
    else:
        form = CategoryForm()
    
    return render(request, 'store/add_category.html', {'form': form})


# Edit Category
def edit_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm(instance=category)

    return render(request, 'store/edit_category.html', {'form': form, 'category': category})


# Delete Category
def delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    if request.method == 'POST':
        category.delete()
        return redirect('categories')
    return render(request, 'store/delete_category.html', {'category': category})

# Check if user is admin
def is_admin(user):
    return user.is_staff

# Admin Dashboard

@login_required
@user_passes_test(is_admin)
def dashboard(request):
    total_products = Product.objects.count()
    total_categories = Category.objects.count()
    total_users = User.objects.count()
    users = User.objects.all()
# Get selected report type
    report_type = request.GET.get('report_type', 'monthly')

    # Define report title
    report_title = "📅 Monthly Sales Report" if report_type == "monthly" else "📆 Yearly Sales Report"

     # Get the current date
    current_date = now()
    # Get sales data based on selection
    if report_type == "monthly":
        start_date = current_date.replace(day=1)  # First day of the current month
        end_date = current_date  # Today's date (to ensure proper filtering)
        total_sales = Order.objects.filter(created_at__year=current_date.year, created_at__month=current_date.month).aggregate(total=Sum('total_price'))['total'] or 0
        total_orders = Order.objects.filter(created_at__year=current_date.year, created_at__month=current_date.month).count()
    else:  # Yearly Report
        start_date = current_date.replace(month=1, day=1)  # First day of the year
        total_sales = Order.objects.filter(created_at__year=current_date.year).aggregate(total=Sum('total_price'))['total'] or 0
        total_orders = Order.objects.filter(created_at__year=current_date.year).count()
        
    context = {
        'users': users,
        'total_products': total_products,
        'total_categories': total_categories,
        'total_users': total_users,
        "report_type": report_type,
        "report_title": report_title,
        "total_sales": total_sales,
        "total_orders": total_orders,
    }
    return render(request, 'store/dashboard.html', context)

# Toggle Staff Status
@login_required
@user_passes_test(is_admin)
def toggle_staff(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == "POST":
        user.is_staff = not user.is_staff
        user.save()
    return redirect('dashboard')

# Delete User
@login_required
@user_passes_test(is_admin)
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == "POST":
        user.delete()
    return redirect('dashboard')

def clear_report(request):
    if request.method == "POST":
        Order.objects.all().delete()  # ⚠️ Deletes all orders!
        messages.success(request, "All orders have been cleared.")
        return redirect('dashboard')
    
def search_results(request):
    query = request.GET.get('q', '')
    products = Product.objects.filter(name__icontains=query) if query else []
    
    return render(request, 'store/search_results.html', {'query': query, 'products': products})
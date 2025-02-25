from django.urls import path
from . import views
from .views import category_list,profile_view, add_product, change_email, edit_product, edit_profile, dashboard
from .views import (
    product_list, product_detail, add_to_cart, 
    cart_view, checkout, order_success, remove_from_cart, update_cart
)
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.views import (
    LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView,
    PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
)

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_view, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('order-success/', views.order_success, name='order_success'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', edit_profile, name='edit_profile'),
    path('add-product/', add_product, name='add_product'),
    
    path('change-email/', change_email, name='change_email'),
    
    path('login/', LoginView.as_view(template_name='store/login.html', next_page='product_list'), name='login'),
    # path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),
    
      # Password Change
    path('password-change/', PasswordChangeView.as_view(template_name='store/password_change.html'), name='password_change'),
    path('password-change/done/', PasswordChangeDoneView.as_view(template_name='store/password_change_done.html'), name='password_change_done'),

    # Password Reset
    path('password-reset/', PasswordResetView.as_view(template_name='store/password_reset.html'), name='password_reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(template_name='store/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='store/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/', PasswordResetCompleteView.as_view(template_name='store/password_reset_complete.html'), name='password_reset_complete'),
    
    
    path('product/<int:product_id>/', product_detail, name='product_detail'),
    path('add-to-cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/', cart_view, name='cart'),
    path('remove-from-cart/<int:cart_item_id>/', remove_from_cart, name='remove_from_cart'),
    path('update-cart/<int:cart_item_id>/', update_cart, name='update_cart'),  # 🆕 Added this
    path('checkout/', checkout, name='checkout'),
    path('order-success/', order_success, name='order_success'),
    path('product/edit/<int:product_id>/', edit_product, name='edit_product'),
    
   path('dashboard/', views.dashboard, name='dashboard'),
   path('categories/', category_list, name='category_list'), 
   path('add-category/', views.add_category, name='add_category'),]

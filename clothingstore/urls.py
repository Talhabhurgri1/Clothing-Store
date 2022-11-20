from django.urls import path 
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    # django default login views 

    path('login', views.login_home, name='login'),
    path('signup', views.signup_home, name='signup'),
    path('logout', views.logout_home, name="logout"),
    
    path('product/<int:pk>', views.product, name='product'),
    path('products', views.products, name='products'),
    path('profile/<int:pk>', views.CustomerProfile, name='customerProfile'),
    path('delete/', views.deleteCustomerOrder, name='deleteOrder'), 

    # admin side 
    path('dashboard', views.dashboard, name='dashboard')  # admin side url 

]

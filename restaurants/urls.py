from orders.views import order_detail
from django.urls import path

from . import views
from location.views import add_restaurant_location
# from coupons.views import add_coupon, update_coupon, delete_coupon


app_name = 'restaurants'

urlpatterns = [
    # urls for customers to view resturants
    path('', views.restaurant_list, name='restaurant_list'),
    path('category/<slug:category_slug>/', views.restaurant_list,
         name='restaurant_list_by_category'),
    path('<int:id>/<slug:slug>/', views.restaurant_detail,
         name='restaurant_detail'),
    # urls for restaurant user to view his/her restaurant
    path('dashboard/', views.restaurant_dashboard,
         name='restaurant_dashboard'),
    path('profile/',
         views.update_restaurant_profile, name='update_profile'),
    path('food/create/', views.FoodCreateView.as_view(), name='create_food'),
    path('food/create/<slug:slug>', views.FoodCreateView.as_view(),
         name='create_food_from_template'),
    path('food/update/<int:pk>/', views.FoodUpdateView.as_view(), name='update_food'),
    path('food/delete/<int:pk>/', views.FoodDeleteView.as_view(), name='delete_food'),
    path('foods/', views.RestaurantFoodListView.as_view(), name='food_list'),
    path('foods/category/<slug:category_slug>/',
         views.RestaurantFoodListView.as_view(), name='foods_list_by_category'),
    path('food/<int:pk>/', views.RestaurantFoodDetailView.as_view(), name='food_detail'),
    # Restaurant Location View
     path('location/', add_restaurant_location, name="add_location"),
     # New Order
     path('new-order/', views.view_new_order, name='view_new_order'),
     path('new-order/read/<int:notification_id>/', views.order_mark_as_read, name='order_mark_as_read'),
     path('new-order/unread/<int:notification_id>/', views.order_mark_as_unread, name='order_mark_as_unread'),
     path('order-detail/<int:notification_id>/', views.order_detail, name='order_detail'),

]

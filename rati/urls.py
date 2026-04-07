from django.urls import path
from .views import *
urlpatterns = [
    path('',index,name="index"),
    path('about/',about,name="about"),
    path('contact/',contact,name="contact"),
    path('rents/',rents,name="rents"),
    path('profile/',profile,name="profile"),
    path('update_profile/',update_profile,name="update_profile"),
    path('change_password/',change_password,name="change_password"),
    path('upload/', upload_product, name='upload_product'),
    path('product/edit/<int:product_id>/',edit_product, name='edit_product'),
    path('soft_delete_property/<int:pk>/',soft_delete_property, name='soft_delete_property'),
    path('search/', product_search, name='product_search'),
    path('product/<int:product_id>/', product_detail, name='product_detail'),
    path('favorites/', favorites_list, name='favorites_list'),
    path('favorite/<int:product_id>/', toggle_favorite, name='toggle_favorite'),
    path('blogs/',blogs,name="blogs"),
    path('privacy/',privacy,name="privacy"),
    path('support/',support,name="support"),

    #auth url part
    path('login/',log_in,name="login"),
    path('register/',register,name="register"),
    path('log_out',log_out,name="log_out"),

]

from django.urls import path
from main.views import show_main, create_product, show_product, show_xml, show_json, show_xml_by_name, show_json_by_name, register, login_user, logout_user, clear_products, edit_product, delete_product, add_product_entry_ajax, edit_product_ajax, delete_product_ajax, register_ajax, login_ajax





app_name = 'main'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('create-product/', create_product, name='create_product'),
    path('product/<str:name>/', show_product, name='show_product'),
    path('xml/', show_xml, name='show_xml'),
    path('json/', show_json, name='show_json'),
    path('xml/<str:product_name>/', show_xml_by_name, name='show_xml_by_name'),
    path('json/<str:product_name>/', show_json_by_name, name='show_json_by_name'),
    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path("clear/", clear_products, name="clear_products"),
    path('product/<str:product_name>/edit', edit_product, name='edit_product'),
    path('product/<str:product_name>/delete', delete_product, name='delete_product'),
    path('create-product-ajax', add_product_entry_ajax, name='add_product_entry_ajax'),
    path('ajax/edit-product/<str:product_name>/', edit_product_ajax, name='edit_product_ajax'),
    path('ajax/delete-product/<str:product_name>/', delete_product_ajax, name='delete_product_ajax'),
    path('register-ajax/', register_ajax, name='register_ajax'),
    path('login-ajax/', login_ajax, name='login_ajax'),
]
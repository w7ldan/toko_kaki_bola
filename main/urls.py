from django.urls import path
from main.views import show_main, create_product, show_product, show_xml, show_json, show_xml_by_name, show_json_by_name, register, login_user, logout_user, clear_products





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
]
from flask import request
from flask_login import current_user
from models import *

def get_form_data():
    product_name = request.form.get('product_name')
    product_description = request.form.get('product_description')
    product_price = request.form.get('price')
    product_stock = request.form.get('stock')
    product_catagory = request.form.get('Catagory')
    return product_name, product_description, product_price, product_stock, product_catagory

def create_product(main_image):
    (product_name,
    product_description,
    product_price,
    product_stock,
    product_catagory) = get_form_data()

    return Products.create(product_name = product_name,
    product_description = product_description,
    product_price = product_price,
    product_stock = product_stock,
    product_create_by_user = current_user,
    product_main_image = main_image,
    catagory = product_catagory)

#change stock of the product
def product_stock_change(product, stock_ammount):
    ...
    

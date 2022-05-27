from flask import request
from flask_login import current_user
from models import *

def get_form_data():
    product_name = request.form.get('product_name')
    product_description = request.form.get('product_description')
    product_price = request.form.get('product_price')
    product_stock = request.form.get('product_stock')
    product_catagory = request.form.get('product_catagory')
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

def edit_product(product_id):
    (product_name,
    product_description,
    product_price,
    product_stock,
    product_catagory) = get_form_data()

    try:
        product = Products.get(Products.product_id == product_id)
        product.product_name = product_name
        product.product_description = product_description
        product.product_price = product_price
        product.product_stock = product_stock
        product.catagory = product_catagory
        product.save()
    except:
        print('something went wrong')

#change stock of the product
def product_stock_change(product, stock_ammount):
    product.product_stock = stock_ammount
    product.save()

#check stock of a product
#return how much we have in stock
def check_product_in_stock(product):
    return product.product_stock
    

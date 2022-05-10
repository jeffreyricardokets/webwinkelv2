from models import *
from flask import request, redirect
from flask_login import current_user
import datetime
from tools import *

def order_items():
    query = Shopping_cart.select().where(Shopping_cart.user == current_user.user_id)
    order_id = make_random_number_generator(10)
    if query.exists():
        for item in query:
            create_order_from_shoppingcart(item , order_id)
            remove_item_from_shoppingcart(item)
        return redirect('/products')


#create new item in the order database
def create_order_from_shoppingcart(item , order_id):
            user = Users.get(Users.user_id == item.user)
            product = Products.get(Products.product_id == item.product)
            Orders.create(user_id = user.user_id, product_id = product.product_id, ammount = item.ammount, order_date = datetime.datetime.now(), order_product_price = product.product_price, order_id = order_id)

#remove the item from the shopping cart
def remove_item_from_shoppingcart(item):
    item.delete_instance()

#get all orders from user
def get_order_list_from_user(user):
    query = Orders.select().where(Orders.user_id == user.user_id)

    #create list
    my_list = []
    if query.exists():
        for item in query:
            my_list.append(item.order_id)
    
    #remove dublicate from list
    user_orders_list = list(dict.fromkeys(my_list))
    #return the order list
    if user_orders_list:
        nested_dict = {}
        i = 1
        for item in user_orders_list:
            order_ammount = 0
            order_item = Orders.select().where(Orders.order_id == item)
            for object in order_item:
                order_date = object.order_date
                order_ammount = order_ammount + (object.ammount * object.order_product_price)
            nested_dict[i] = {'order_id' : item, 'order_date' : order_date, 'order_ammount' : order_ammount}
            i = i + 1
        return nested_dict
    else:
        #return to the customer that he did not order something yet
        print('order list is empty')

#get items from order
def get_order_from_id(order_id):
    query = Orders.select(Products.product_name, Orders).join(Products, attr='product').where(order_id == order_id)
    if query.exists():
        return query

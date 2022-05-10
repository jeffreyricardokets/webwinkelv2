from numpy import product
from peewee import *

db = SqliteDatabase('app.db')

class BaseModel(Model):
    class Meta:
        database = db

#user
class Users(BaseModel):
    user_id = PrimaryKeyField()
    user_first_name = CharField()
    user_last_name = CharField()
    user_email_address = CharField()
    user_username = CharField(unique = True)
    user_password = CharField()
    user_join_date = DateTimeField()
    is_authenticated = BooleanField()
    is_active = BooleanField()
    is_anonymous = BooleanField()
    is_admin = BooleanField()

#Images store all the images of our website
class Images(BaseModel):
    img_location = CharField()

#catagories
class Catagories(BaseModel):
    catagory_name = CharField()
    created_by = ForeignKeyField(Users)

#product
class Products(BaseModel):
    product_id = PrimaryKeyField()
    product_name = CharField()
    product_description = CharField()
    product_price = FloatField()
    product_stock = IntegerField()
    product_create_by_user = ForeignKeyField(Users)
    product_main_image = ForeignKeyField(Images)
    catagory = ForeignKeyField(Catagories)

#connect the images to the products
class Product_images(BaseModel):
    product = ForeignKeyField(Products)
    image = ForeignKeyField(Images)    

#shopping_list
class Shopping_cart(BaseModel):
    user = ForeignKeyField(Users)
    product = ForeignKeyField(Products)
    ammount = IntegerField()
    cart_product_price = FloatField()

class Orders(BaseModel):
    user = ForeignKeyField(BaseModel)
    product = ForeignKeyField(Products)
    ammount = IntegerField()
    order_date = DateField()
    order_id = CharField()
    order_product_price =  FloatField()
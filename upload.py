from models import *
import os
import pathlib
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from tools import *

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

server_file_path = pathlib.Path(__file__).parent.resolve()
upload_folder = server_file_path / 'static' / 'uploads'
products_folder = upload_folder / 'products'
img_product_folder = products_folder / 'images'

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#check if all the upload folders exists
def check_if_upload_folders_exist():
    if not os.path.isdir(upload_folder):
        os.mkdir(upload_folder)
        os.mkdir(products_folder)
        os.mkdir(img_product_folder)
    else:
        if not os.path.isdir(products_folder):
            os.mkdir(products_folder)
            os.mkdir(img_product_folder)
        else:
            if not os.path.isdir(img_product_folder):
                os.mkdir(img_product_folder)
    
#upload file to our storage
def upload_product_image(file, app):
    #list of all images
    img_list = []
    #make the random string for the map name
    file_folder = make_random_text_generator(50)
    #check if the map name exists
    check_if_folder_exists(app.config['UPLOAD_FOLDER'] / file_folder)
    for f in request.files.getlist('file'):
        filename = secure_filename(f.filename)
        file_location = (os.path.join(app.config['UPLOAD_FOLDER'] / file_folder , filename))
        f.seek(0)
        f.save(os.path.join(file_location))
        img_list.append (upload_product_image_link(file_location).id)
    return img_list

#create a record in the database where the img hase been uploaded so we can recall it
def upload_product_image_link(file_location):
    path = (os.path.relpath(file_location, server_file_path / 'static'))
    image = Images.create(img_location = path)
    return image

#make a row in our database to tell which product should have which image
def connect_img_to_product(image,product):
    Product_images.create(product = product, image = image)

def check_if_folder_exists(folder):
    if not os.path.exists(folder):
        os.mkdir(folder)


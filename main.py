from crypt import methods
from unicodedata import category
from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_login import LoginManager, login_required, logout_user, current_user
from models import *
import account
import products as product_script
import upload
import orders
import catagory

__winc_id__ = "9263bbfddbeb4a0397de231a1e33240a"
__human_name__ = "templates"

db.create_tables([Users,Products, Images, Product_images, Shopping_cart, Orders, Catagories])

app = Flask(__name__)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config['UPLOAD_FOLDER'] = upload.img_product_folder
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

login_manager = LoginManager()
login_manager.init_app(app)

query_catagories = catagory.query_all_in_catagories()

@app.route("/")
def index():
    return render_template('index.html', title='index', query_catagories = query_catagories)

@app.route('/home')
@app.route('/index')
def home():
    return redirect('/', query_catagories = query_catagories)

@app.route('/products')
def products():
    query_products = Products.select(Images.img_location, Products).join(Images, attr='image').where(Images.id == Products.product_main_image)
    return render_template('shop.html', products = query_products , query_catagories = query_catagories)

@app.route('/account')
def login():
    if current_user.is_authenticated:
        return redirect('user/dashboard')
    else:
        return render_template('account.html')

@app.route('/register' , methods=['POST'])
def register():
    return account.create_user()

@app.route('/login', methods = ['POST'])
def user_login():
    return redirect(account.login_user())



@app.route('/orders')
@login_required
def show_orders():
    items = orders.get_order_list_from_user(current_user)
    return render_template('orders.html', items = items, query_catagories = query_catagories)

@app.route('/user/dashboard', methods = ['GET'])
@login_required
def user_dashboard():
    return render_template('userdashboard.html', query_catagories = query_catagories)

@app.route('/products/<product_id>', methods = ['GET'])
def show_product(product_id):
    query = Products.select().where(Products.product_id == product_id)
    if query.exists():
        query_product = Products.get(product_id = product_id)
        images = Product_images.select(Product_images,Images.img_location).join(Images, attr='p_img').where(Product_images.product == product_id)
        return render_template('product.html', product = query_product , images = images, query_catagories = query_catagories)
    else:
        return '<h1>Id not found</h1>'


@app.route('/addtocard', methods = ['POST'])
@login_required
def add_to_cart():
    quantity_input = request.form.get('quantity')
    product_input = request.form.get('product_id')
    product = Products.get(Products.product_id == product_input)
    Shopping_cart.create(product = product.product_id , user = current_user, ammount = quantity_input, cart_product_price = product.product_price)
    return redirect('/products')

@app.route('/order_items', methods = ['POST'])
@login_required
def add_order():
    orders.order_items()
    return redirect('/orders')

@app.route('/cart')
@login_required
def show_cart():
    query = Shopping_cart.select(Products.product_name,Shopping_cart).join(Products, attr='product').where(Shopping_cart.user == current_user.user_id)
    return render_template('cart.html', query = query, query_catagories = query_catagories)

@app.route('/cart/remove_item/<item_id>', methods= ['POST'])
@login_required
def remove_item(item_id):
    item = Shopping_cart.get(Shopping_cart.id == item_id)
    item.delete_instance()
    return redirect('/cart')


@app.route('/search', methods = ['POST'])
def search_product():
    search_item = request.form.get('Search')
    query_products = Products.select(Images.img_location, Products).join(Images, attr='image').where(Images.id == Products.product_main_image, Products.product_name ** search_item)
    return render_template('shop.html', products = query_products)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect('/')

#Admin routes
@app.route('/admin/create-item', methods= ['GET'])
@login_required
def create_item():
    if current_user.is_admin:
        catagory_query = catagory.query_all_in_catagories()
        if catagory_query:
            return render_template('create_product.html', catagory_query = catagory_query)
        else:
            return ''
    else:
        return 'you are not an admin'

@app.route('/admin/create-item', methods = ['POST'])
@login_required
def create_item_in_db():
    if 'file' not in request.files:
        print('no file')
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        print('no image')
        flash('No image selected for uploading')
        return redirect(request.url)

    if file and upload.allowed_file(file.filename):
        images = upload.upload_product_image(file, app)
        product = product_script.create_product(images[0])
        for image in images:
            upload.connect_img_to_product(image,product)
        return redirect('../products')
    else:
        print('mage successfully uploaded and displayed below')
        flash('Allowed image types are -> png, jpg, jpeg, gif')
        return redirect(request.url)

@app.route('/admin/create-catagory', methods = ['GET'])
@login_required
def create_catagory_form():
    if current_user.is_admin:
        return render_template('create_catagory.html')
    else:
        return 'you are not an admin'



@app.route('/admin/create-catagory', methods = ['POST'])
@login_required
def create_catagory():
    if catagory.create_catagory():
        return 'Catagory created'
    else:
        return 'Could not make the product'

@app.route('/admin/dashboard', methods = ['GET'])
@login_required
def show_admin_dashboard():
    if current_user.is_admin:
        return render_template('admin_dashboard.html')



@login_manager.user_loader
def load_user(user_id):
    return Users.get(user_id)

if __name__ == '__main__':
    upload.check_if_upload_folders_exist()
    app.run(port=65008, debug=True)


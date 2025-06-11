from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)

# MongoDB setup
client = MongoClient('mongodb+srv://kowmudhibattula:KOWMU-2006@cluster0.jdurkkm.mongodb.net/')
db = client['zerohunger']
customers = db['customers']
restaurants = db['restaurants']
orders = db['orders']
menu_items = db['menu_items']
carts = db['carts']
products_collection = db['products']

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/customer_login', methods=['GET', 'POST'])
def customer_login():
    if request.method == 'POST':
        customer = {
            'name': request.form['name'],
            'email': request.form['email']
        }
        customers.insert_one(customer)
        return redirect(url_for('products', email=customer['email']))
    return render_template('customer_login.html')

@app.route('/restaurant_login', methods=['GET', 'POST'])
def restaurant_login():
    if request.method == 'POST':
        restaurant = {
            'restaurant_name': request.form['restaurant_name'],
            'address': request.form['address'],
            'customer_care': request.form['customer_care'],
            'email': request.form['email']
        }
        restaurants.insert_one(restaurant)
        return redirect(url_for('products', email=restaurant['email']))
    return render_template('restaurant_login.html')

@app.route('/online_orders', methods=['GET', 'POST'])
def online_orders():
    if request.method == 'POST':
        order = {
            'customer_email': request.form['email'],
            'delivery_method': request.form['delivery_method'],
            'address': request.form['address']
        }
        orders.insert_one(order)
        return redirect(url_for('my_orders'))
    return render_template('online_orders.html')

@app.route('/menus')
def menus():
    menu_items = {
        "Starters": [
            {"name": "Veg Spring Rolls", "desc": "Crispy rolls stuffed with mixed vegetables and lightly spiced.", "price": "₹60", "img": "images/vegrolls.jpg"},
            {"name": "Chicken Lollipop", "desc": "Fried chicken wings marinated with garlic and chili sauce.", "price": "₹120", "img": "images/chilol.jpg"}
        ],
        "Main Course": [
            {"name": "Paneer Butter Masala", "desc": "Cottage cheese cubes simmered in creamy tomato-based gravy.", "price": "₹150", "img": "images/panner.jpg"},
            {"name": "Chicken Biryani", "desc": "Aromatic basmati rice layered with marinated chicken and spices.", "price": "₹180", "img": "images/chibir.jpg"}
        ],
        "Snacks": [
            {"name": "Veg Puff", "desc": "Flaky pastry filled with spiced vegetables.", "price": "₹25", "img": "images/vegpuff.jpg"},
            {"name": "Samosa", "desc": "Deep-fried pastry with spicy potato and peas filling.", "price": "₹20", "img": "images/samosa.jpg"}
        ]
    }
    return render_template("menus.html", menu_items=menu_items)

@app.route('/products')
def products():
    email = request.args.get('email', 'demo@example.com')  # Default email for testing
    product_list = list(products_collection.find())
    return render_template('products.html', products=product_list, email=email)

@app.route('/add_product', methods=['POST'])
def add_product():
    product = {
        'name': request.form['name'],
        'price': float(request.form['price']),
        'preparation_time': request.form['preparation_time'],
        'expiry_date': request.form['expiry_date'],
        'image': request.form['image']
    }
    products_collection.insert_one(product)
    return redirect(url_for('products'))

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    product_id = request.form['product_id']
    customer_email = request.form['customer_email']

    product = products_collection.find_one({'_id': ObjectId(product_id)})
    if product:
        cart_item = {
            'customer_email': customer_email,
            'product_id': product_id,
            'product_name': product['name'],
            'price': float(product['price']),  # make sure price is stored properly
            'quantity': 1
        }
        carts.insert_one(cart_item)
    return redirect(url_for('cart', email=customer_email))
@app.route('/cart')
def cart():
    email = request.args.get('email')  # Email passed via query parameter
    user_cart = list(carts.find({'customer_email': email}))

    # Use .get to avoid KeyError if fields are missing
    total = sum(float(item.get('price', 0)) * int(item.get('quantity', 1)) for item in user_cart)

    return render_template('cart.html', cart=user_cart, email=email, total=total)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/my_orders')
def my_orders():
    user_orders = list(orders.find())
    return render_template('my_orders.html', orders=user_orders)

if __name__ == '__main__':
    app.run(debug=True)

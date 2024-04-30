# Importing necessary modules and libraries
from flask import render_template, flash, url_for, request, current_app, jsonify
from datetime import datetime
from sqlalchemy import or_, func
import sqlalchemy as sa

# Importing database models and blueprint
from app import db
from app.models.product import Product
from app.models.user import User
from app.models.reward import Reward
from app.products import bp

# Importing login manager
from flask_login import current_user, login_required
from sqlalchemy.sql.operators import like_op

# Route for selling products
@bp.route('/sell')
@login_required
def sell():
    # Retrieving page number and search query from request arguments
    page = request.args.get('page', 1, type=int)
    search_string = request.args.get('q')

    # Creating query to retrieve products that are not sold and are listed by the current user
    query = sa.select(Product, User).join(User, User.id == Product.seller_id).where(Product.is_sold == False, Product.seller_id == current_user.id)
    products = apply_search_and_paginate(query, search_string, page)

    # Generating URLs for pagination
    next_url = url_for('products.sell', page=products.next_num) if products.has_next else None
    prev_url = url_for('products.sell', page=products.prev_num) if products.has_prev else None

    # Rendering sell page with products and pagination links
    return render_template('products/sell.html', title='Sell items', searchPath=url_for('products.sell'),
                           products=products.items, next_url=next_url,
                           prev_url=prev_url)

# Route for generating a new product
@bp.route('/generate_product', methods=['POST'])
@login_required
def generate_product():
    # Retrieving JSON data from request
    data = request.get_json()
    
    # Checking if JSON data is present
    if not data:
        return jsonify({'success': False, 'message': 'No data received'}), 400

    # Extracting product details from JSON data
    name = data.get('name')
    category = data.get('category')
    price = data.get('price')

    # Checking if price exceeds $10
    if int(price) > 10:
        return jsonify({'success': False, 'message': 'Price cannot exceed $10'}), 400

    # Creating new product object with extracted details
    product = Product(name=name, category=category, price=price, seller_id=current_user.id)
    product.image = product.generate_image(product.category)

    # Checking if image generation was successful
    if product.image is None:
        flash('Error during the image generation, try again later!')
        return

    # Adding product to the database
    db.session.add(product)
    db.session.commit()

    # Deducting reward points for generating image and updating user's money balance
    Reward.deductRewardForImageGeneration(current_user.id, product.id)

    # Returning JSON response with product details
    return jsonify({
        "success": True,
        "message": "Congratulations, your product has been generated!",
        "data": {
            "id": product.id,
            "name": product.name,
            "category": product.category,
            "price": product.price,
            "image": product.image,
            "timestamp": product.timestamp.strftime('%Y-%m-%d'),
            "username": current_user.username,
            "avatar": current_user.avatar(24)
        }
    }), 201

# Route for viewing available products for purchase
@bp.route('/buy')
@login_required
def buy():
    # Retrieving page number and search query from request arguments
    page = request.args.get('page', 1, type=int)
    search_string = request.args.get('q')

    # Creating query to retrieve products that are not sold
    query = sa.select(Product, User).join(User, User.id == Product.seller_id).where(Product.is_sold == False)
    products = apply_search_and_paginate(query, search_string, page)

    # Generating URLs for pagination
    next_url = url_for('products.buy', page=products.next_num) if products.has_next else None
    prev_url = url_for('products.buy', page=products.prev_num) if products.has_prev else None

    # Rendering buy page with products and pagination links
    return render_template('products/buy.html', title='Buy', products=products.items, next_url=next_url, prev_url=prev_url)

# Route for purchasing a product
@bp.route('/<product_id>/buy', methods=['GET'])
@login_required
def buy_product(product_id):
    # Retrieving product with given ID if it's not sold yet
    product = db.first_or_404(sa.select(Product).where(Product.id == product_id, Product.is_sold == False))

    # Checking if the buyer is the seller
    if (product.seller_id == current_user.id):
        return jsonify({"success": False, "message": "Sorry, you cannot purchase an item that you've created."}), 422

    # Checking if the buyer has enough money to buy the product
    if (int(round(product.price)) > current_user.money):
        return jsonify({"success": False, "message": "Sorry, you do not have enough money to buy this product"}), 200

    # Updating product details to mark it as sold
    product.is_sold = True
    product.buyer_id = current_user.id
    product.sold_at = datetime.utcnow()
    db.session.commit()

    # Deducting reward points for purchase and updating user's money balance
    Reward.deductRewardForPurchase(current_user.id, product.id, int(round(product.price)))

    # Adding reward points for multiple purchases from same user or category
    Reward.addRewardForPurchaseFromSameUserIfApplicable(current_user.id, product.id, product.seller_id)
    Reward.addRewardForPurchaseFromSameUserIfApplicable(current_user.id, product.id, product.category)

    # Returning success message in JSON format
    return jsonify({"success": True, "message": "Congratulations, your product purchase has been completed successfully!"}), 200

# Route for viewing purchased products
@bp.route('/my_purchases')
@login_required
def my_purchases():
    # Retrieving page number and search query from request arguments
    page = request.args.get('page', 1, type=int)
    search_string = request.args.get('q')

    # Creating query to retrieve products that are sold and bought by the current user
    query = sa.select(Product, User).join(User, User.id == Product.seller_id).where(Product.is_sold == True, Product.buyer_id == current_user.id)
    products = apply_search_and_paginate(query, search_string, page)

    # Generating URLs for pagination
    next_url = url_for('products.my_purchases', page=products.next_num) if products.has_next else None
    prev_url = url_for('products.my_purchases', page=products.prev_num) if products.has_prev else None

    # Rendering my_purchases page with products and pagination links
    return render_template('products/my_purchases.html', title='My purchases', searchPath = url_for('products.my_purchases'), 
                           products=products.items, next_url=next_url,
                           prev_url=prev_url)

# Function to apply search and pagination to a given query
def apply_search_and_paginate(query, search_string, page):
    if search_string:
        # Adding search filters to the query
        query = query.where(
            or_(
                func.lower(Product.name).like('%' + search_string.lower() + '%'),
                func.lower(Product.category).like('%' + search_string.lower() + '%')
            )
        )
    
    # Ordering query results by timestamp in descending order
    query = query.order_by(Product.timestamp.desc())

    # Paginating query results and returning them
    return db.paginate(query, page=page, per_page=current_app.config['POSTS_PER_PAGE'], error_out=False)

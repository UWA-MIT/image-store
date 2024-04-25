from flask import render_template, flash, url_for, request, current_app, jsonify
from datetime import datetime
from sqlalchemy import or_, func
import sqlalchemy as sa

from app import db
from app.models.product import Product
from app.models.user import User
from app.products import bp


from flask_login import current_user, login_required
from sqlalchemy.sql.operators import like_op


@bp.route('/sell')
@login_required
def sell():
    page = request.args.get('page', 1, type=int)
    search_string = request.args.get('q')

    query = sa.select(Product, User).join(User, User.id == Product.seller_id).where(Product.is_sold == False, Product.seller_id == current_user.id)
    products = apply_search_and_paginate(query, search_string, page)

    next_url = url_for('products.sell', page=products.next_num) \
        if products.has_next else None
    prev_url = url_for('products.sell', page=products.prev_num) \
        if products.has_prev else None
    return render_template('products/sell.html', title='Sell items', searchPath=url_for('products.sell'),
                           products=products.items, next_url=next_url,
                           prev_url=prev_url)



@bp.route('/generate_product', methods=['POST'])
@login_required
def generate_product():

    data = request.get_json()
    
    if not data:
        return jsonify({'success': False, 'message': 'No data received'}), 400

    name = data.get('name')
    category = data.get('category')
    price = data.get('price')

    if int(price) > 10:
        return jsonify({'success': False, 'message': 'Price cannot exceed $10'}), 400

    product = Product(name=name, category=category, price=price, seller_id=current_user.id)
    product.image = product.generate_image(product.category)

    if product.image is None:
        flash('Error during the image generation, try again later!')
        return

    db.session.add(product)

    user = db.session.get(User, current_user.id)
    user.money = user.money + int(current_app.config['REWARD_MONEY_FOR_GENERATE_PRODUCT'])

    db.session.commit()

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
            "username": user.username,
            "avatar": user.avatar(24)
        }
    }), 201


@bp.route('/buy')
@login_required
def buy():

    page = request.args.get('page', 1, type=int)
    search_string = request.args.get('q')

    query = sa.select(Product, User).join(User, User.id == Product.seller_id).where(Product.is_sold == False)
    products = apply_search_and_paginate(query, search_string, page)

    next_url = url_for('products.buy', page=products.next_num) \
        if products.has_next else None
    prev_url = url_for('products.buy', page=products.prev_num) \
        if products.has_prev else None
    return render_template('products/buy.html', title='Buy', products=products.items, next_url=next_url, prev_url=prev_url)


@bp.route('/<product_id>/buy', methods=['GET'])
@login_required
def buy_product(product_id):
    product = db.first_or_404(sa.select(Product).where(Product.id == product_id, Product.is_sold == False))

    if (product.seller_id == current_user.id):
        return jsonify({"success": False, "message": "Sorry, you cannot purchase an item that you've created."}), 422

    if (int(round(product.price)) > current_user.money):
        return jsonify({"success": False, "message": "Sorry, you do not have enough money to buy this product"}), 200

    product.is_sold = True
    product.buyer_id = current_user.id
    product.sold_at = datetime.utcnow()

    user = db.session.get(User, current_user.id)
    user.money = user.money - int(round(product.price))
    db.session.commit()
    return jsonify({"success": True, "message": "Congratulations, your product purchase has been completed successfully!"}), 200

@bp.route('/my_purchases')
@login_required
def my_purchases():
    page = request.args.get('page', 1, type=int)
    search_string = request.args.get('q')

    query = sa.select(Product, User).join(User, User.id == Product.seller_id).where(Product.is_sold == True, Product.buyer_id == current_user.id)
    products = apply_search_and_paginate(query, search_string, page)

    next_url = url_for('products.my_purchases', page=products.next_num) \
        if products.has_next else None
    prev_url = url_for('products.my_purchases', page=products.prev_num) \
        if products.has_prev else None
    return render_template('products/my_purchases.html', title='My purchases', searchPath = url_for('products.my_purchases'), 
                           products=products.items, next_url=next_url,
                           prev_url=prev_url)

def apply_search_and_paginate(query, search_string, page):
    if search_string:
        query = query.where(
            or_(
                func.lower(Product.name).like('%' + search_string.lower() + '%'),
                func.lower(Product.category).like('%' + search_string.lower() + '%')
            )
        )
    query = query.order_by(Product.timestamp.desc())
    return db.paginate(query, page=page, per_page=current_app.config['POSTS_PER_PAGE'], error_out=False)
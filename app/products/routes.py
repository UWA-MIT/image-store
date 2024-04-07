from flask import render_template, url_for, flash, redirect, request, current_app, jsonify
from datetime import datetime
import sqlalchemy as sa

from app import db
from app.models.product import Product
from app.models.user import User
from app.products import bp
from flask_login import login_required, current_user


@bp.route('/buy')
@login_required
def buy():

    page = request.args.get('page', 1, type=int)

    query = sa.select(Product, User).join(User, User.id == Product.seller_id).where(Product.is_sold == False).order_by(Product.timestamp.desc())

    products = db.paginate(query, page=page, per_page=current_app.config['POSTS_PER_PAGE'], error_out=False)

    next_url = url_for('products.buy', page=products.next_num) \
        if products.has_next else None
    prev_url = url_for('products.buy', page=products.prev_num) \
        if products.has_prev else None
    return render_template('products/buy.html', title='Buy', products=products.items, next_url=next_url, prev_url=prev_url)


@bp.route('/<product_id>/buy', methods=['GET'])
@login_required
def buy_product(product_id):
    product = db.first_or_404(sa.select(Product).where(Product.id == product_id, Product.is_sold == False))

    if (int(round(product.price)) > current_user.reward_points):
        return jsonify({"success": False, "message": "Sorry, you do not have enough reward points to buy this product"}), 200

    product.is_sold = True
    product.buyer_id = current_user.id
    product.sold_at = datetime.utcnow()

    user = db.session.get(User, current_user.id)
    user.reward_points = user.reward_points - int(round(product.price))
    db.session.commit()
    return jsonify({"success": True, "message": "Congratulations, your product purchase has been completed successfully!"}), 200

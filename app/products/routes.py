from flask import render_template, flash, redirect, url_for, request, current_app, jsonify
from urllib.parse import urlsplit
from datetime import datetime, timezone
import sqlalchemy as sa
from  sqlalchemy.orm  import joinedload
from sqlalchemy.sql.operators import like_op


# from app import app
from app import db
from app.models.product import Product
from app.models.user import User
from app.products import bp

from flask_login import current_user, login_user, logout_user, login_required
from app.products.forms import GenerateProductForm


@bp.route('/')
@bp.route('/index')
@login_required
def index():

    searchString = request.args.get('q')
    page = request.args.get('page', 1, type=int)
    q = None
    title = 'Buy'

    if (searchString):
        query = sa.select(Product, User).join(User, User.id == Product.seller_id).where(Product.is_sold == False, \
                        like_op(Product.name, '%' + searchString + '%')).order_by(Product.timestamp.desc())
        q = searchString
        title = "Search: " + q
    else:
        query = sa.select(Product, User).join(User, User.id == Product.seller_id).where(Product.is_sold == False).order_by(Product.timestamp.desc())

    products = db.paginate(query, page=page, per_page=current_app.config['POSTS_PER_PAGE'], error_out=False)



    next_url = url_for('products.index', q=q, page=products.next_num) \
        if products.has_next else None
    prev_url = url_for('products.index', q=q, page=products.prev_num) \
        if products.has_prev else None
    return render_template('products/index.html', title=title,
                           products=products.items, next_url=next_url,
                           prev_url=prev_url)

@bp.route('/sell')
@login_required
def sell():
    page = request.args.get('page', 1, type=int)

    query = sa.select(Product, User).join(User, User.id == Product.seller_id).where(Product.is_sold == False, Product.seller_id == current_user.id).order_by(Product.timestamp.desc())

    products = db.paginate(query, page=page, per_page=current_app.config['POSTS_PER_PAGE'], error_out=False)

    next_url = url_for('products.sell', page=products.next_num) \
        if products.has_next else None
    prev_url = url_for('products.sell', page=products.prev_num) \
        if products.has_prev else None
    return render_template('products/sell.html', title='Sell items',
                           products=products.items, next_url=next_url,
                           prev_url=prev_url)



@bp.route('/generate_product', methods=['GET', 'POST'])
@login_required
def generate_product():

    form = GenerateProductForm()
    if form.validate_on_submit():
        product = Product(name=form.name.data, description=form.description.data, price = form.price.data, seller_id = current_user.id)
        product.image = Product.generate_image(product.name)
        # logger.info("Image OpenAI: " . product.image)

        db.session.add(product)

        user = db.session.get(User, current_user.id)
        user.reward_points = user.reward_points + int(current_app.config['REWARD_POINTS_FOR_GENERATE_PRODUCT'])

        db.session.commit()

        flash('Congratulations, your product has been generated.')
        return redirect(url_for('products.sell'))

    return render_template('products/generate_product.html', title='Generate Product',
                           form=form)


from flask import render_template, url_for, request, current_app
import sqlalchemy as sa
from app import db
from app.models.product import Product
from app.models.user import User
from app.products import bp
from flask_login import login_required


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

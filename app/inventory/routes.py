from flask import render_template
from flask_login import login_required, current_user
from . import inventoryBp
from ..models import ProductVariant, Movement

@inventoryBp.route('/')
@login_required #The route must be protected
def dashboard():
    userName = current_user.person.name
    return render_template('inventoryDashboard.html', userName=userName)

@inventoryBp.route('/products')
@login_required
def listProducts():
    products=ProductVariant.query.all()
    return render_template('productsList.html', products=products)

@inventoryBp.route('/kardex/<int:productVariantId>')
@login_required
def viewKardex(productVariantId):
    product=ProductVariant.query.get_or_404(productVariantId)
    movements=Movement.query.filter_by(productVariantId=productVariantId).order_by(Movement.createdAt.asc()).all()
    
    return render_template('kardexView.html',product=product, movements=movements)
    
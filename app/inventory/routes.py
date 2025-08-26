from flask import render_template
from flask_login import login_required, current_user
from . import inventoryBp

@inventoryBp.route('/')
@login_required #The route must be protected
def dashboard():
    userName = current_user.person.name
    return render_template('inventoryDashboard.html', userName=userName)
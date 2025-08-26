from flask import redirect, url_for
from flask_login import current_user
from . import mainBp

@mainBp.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('inventory.dashboard'))
    
    return redirect(url_for('auth.login'))
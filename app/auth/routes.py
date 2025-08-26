from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from . import authBp
from ..models import User

@authBp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('inventory.dashboard'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(userEmail=email).first()
        
        if user and user.check_password(password):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('inventory.dashboard'))
        else:
            flash('Correo o contraseña incorrectos. Por favor, intente de nuevo.', 'danger')
    return render_template('login.html')

@authBp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Ha cerrado sesión exitosamente.', 'success')
    return redirect(url_for('auth.login'))
from flask import render_template
from . import auth_bp

@auth_bp.route('/')
def login():
    return render_template('index.html')
from flask import Blueprint

authBp = Blueprint(
    'auth', 
    __name__,
    template_folder='templates',
    static_folder='static'
)

from . import routes
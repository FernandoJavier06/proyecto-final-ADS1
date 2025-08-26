from flask import Blueprint

mainBp = Blueprint('main', 
                   __name__)

from . import routes
from flask import Blueprint

inventoryBp = Blueprint(
    'inventory',
    __name__,
    template_folder='templates'
)

from . import routes
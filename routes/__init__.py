from flask import Blueprint

# Blueprint para as rotas
bp = Blueprint('routes', __name__)

@bp.route('/forbidden')
def forbidden():
    return render_template('403.html'), 403


from .usuarios import *
from .index import *
from .login import *
from .livros import *
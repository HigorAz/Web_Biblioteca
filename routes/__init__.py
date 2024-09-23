from flask import Blueprint

# Blueprint para as rotas
bp = Blueprint('routes', __name__)

from .usuarios import *
from .index import *
from .login import *
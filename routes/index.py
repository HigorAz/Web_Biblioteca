from flask import render_template, request, jsonify
from . import bp
from db.database import get_db

@bp.route('/')
def home():
    return render_template ("base.html")
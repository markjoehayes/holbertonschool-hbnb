from flask import Blueprint, render_template

# Create a blueprint for web routes
bp = Blueprint('web', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/login')
def login():
    return render_template('login.html')

@bp.route('/place/<place_id>')
def place_details(place_id):
    return render_template('place.html', place_id=place_id)

@bp.route('/place/<place_id>/add_review')
def add_review(place_id):
    return render_template('add_review.html', place_id=place_id)

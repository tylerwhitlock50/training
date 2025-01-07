import requests
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app.extensions import db
from app.models import User
from app.utils import requires_role


training = Blueprint('trainings', __name__, url_prefix='/trainings')

@training.route('/create', methods=['GET', 'POST'])
@login_required
@requires_role('admin')
def create_training():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description


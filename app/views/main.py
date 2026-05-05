from flask import Blueprint, redirect, url_for, session
from flask_login import login_required

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
@login_required
def index():
    return redirect(url_for('contacts.index'))


@main_bp.route('/lang/<lang_code>')
def set_language(lang_code):
    from flask import request
    session['lang'] = lang_code
    return redirect(request.referrer or url_for('main.index'))

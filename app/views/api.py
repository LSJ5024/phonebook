from flask import Blueprint, jsonify, request
from flask_login import login_required
from app import db
from app.models.contact import Contact
from app.models.category import Category
from app.models.tag import Tag

api_bp = Blueprint('api', __name__)


@api_bp.route('/contacts')
@login_required
def list_contacts():
    q = request.args.get('q', '').strip()
    query = Contact.query.filter_by(is_active=True)
    if q:
        like = f'%{q}%'
        query = query.filter(
            db.or_(Contact.name.ilike(like), Contact.organization.ilike(like),
                   Contact.phone.ilike(like), Contact.mobile.ilike(like))
        )
    contacts = query.order_by(Contact.name).limit(100).all()
    return jsonify([c.to_dict() for c in contacts])


@api_bp.route('/contacts/<int:contact_id>')
@login_required
def get_contact(contact_id):
    contact = Contact.query.get_or_404(contact_id)
    return jsonify(contact.to_dict())


@api_bp.route('/categories')
@login_required
def list_categories():
    cats = Category.query.order_by('name').all()
    return jsonify([{'id': c.id, 'name': c.name, 'color': c.color} for c in cats])


@api_bp.route('/tags')
@login_required
def list_tags():
    tags = Tag.query.order_by('name').all()
    return jsonify([{'id': t.id, 'name': t.name, 'color': t.color} for t in tags])

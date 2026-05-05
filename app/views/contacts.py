import io
import os
import uuid
from flask import (Blueprint, render_template, redirect, url_for, flash,
                   request, current_app, send_file, Response)
from flask_login import login_required, current_user
from app import db
from app.models.contact import Contact
from app.models.category import Category
from app.models.tag import Tag
from app.forms.contact import ContactForm, ImportForm
from app.utils import log_action, parse_import_file, COLUMN_MAP

contacts_bp = Blueprint('contacts', __name__)


def _populate_form_choices(form):
    form.categories.choices = [(c.id, c.name) for c in Category.query.order_by('name')]
    form.tags.choices = [(t.id, t.name) for t in Tag.query.order_by('name')]


@contacts_bp.route('/')
@login_required
def index():
    page = request.args.get('page', 1, type=int)
    q = request.args.get('q', '').strip()
    category_id = request.args.get('category', type=int)
    tag_id = request.args.get('tag', type=int)

    query = Contact.query.filter_by(is_active=True)

    if q:
        like = f'%{q}%'
        query = query.filter(
            db.or_(
                Contact.name.ilike(like),
                Contact.phone.ilike(like),
                Contact.mobile.ilike(like),
                Contact.email.ilike(like),
                Contact.organization.ilike(like),
                Contact.department.ilike(like),
            )
        )
    if category_id:
        query = query.filter(Contact.categories.any(Category.id == category_id))
    if tag_id:
        query = query.filter(Contact.tags.any(Tag.id == tag_id))

    pagination = query.order_by(Contact.name).paginate(page=page, per_page=20, error_out=False)
    categories = Category.query.order_by('name').all()
    tags = Tag.query.order_by('name').all()

    return render_template('contacts/index.html',
                           contacts=pagination.items,
                           pagination=pagination,
                           categories=categories,
                           tags=tags,
                           q=q,
                           selected_category=category_id,
                           selected_tag=tag_id)


@contacts_bp.route('/new', methods=['GET', 'POST'])
@login_required
def create():
    form = ContactForm()
    _populate_form_choices(form)
    if form.validate_on_submit():
        contact = Contact(
            name=form.name.data,
            phone=form.phone.data,
            mobile=form.mobile.data,
            email=form.email.data,
            organization=form.organization.data,
            department=form.department.data,
            position=form.position.data,
            address=form.address.data,
            memo=form.memo.data,
            created_by=current_user.id,
        )
        contact.categories = Category.query.filter(Category.id.in_(form.categories.data)).all()
        contact.tags = Tag.query.filter(Tag.id.in_(form.tags.data)).all()
        db.session.add(contact)
        db.session.commit()
        log_action('create', 'contact', contact.id, contact.name)
        flash('연락처가 추가되었습니다.', 'success')
        return redirect(url_for('contacts.index'))
    return render_template('contacts/form.html', form=form, title='연락처 추가')


@contacts_bp.route('/<int:contact_id>')
@login_required
def detail(contact_id):
    contact = Contact.query.get_or_404(contact_id)
    return render_template('contacts/detail.html', contact=contact)


@contacts_bp.route('/<int:contact_id>/edit', methods=['GET', 'POST'])
@login_required
def edit(contact_id):
    contact = Contact.query.get_or_404(contact_id)
    form = ContactForm(obj=contact)
    _populate_form_choices(form)

    if request.method == 'GET':
        form.categories.data = [c.id for c in contact.categories]
        form.tags.data = [t.id for t in contact.tags]

    if form.validate_on_submit():
        form.populate_obj(contact)
        contact.categories = Category.query.filter(Category.id.in_(form.categories.data)).all()
        contact.tags = Tag.query.filter(Tag.id.in_(form.tags.data)).all()
        db.session.commit()
        log_action('update', 'contact', contact.id, contact.name)
        flash('연락처가 수정되었습니다.', 'success')
        return redirect(url_for('contacts.detail', contact_id=contact.id))
    return render_template('contacts/form.html', form=form, title='연락처 수정', contact=contact)


@contacts_bp.route('/<int:contact_id>/delete', methods=['POST'])
@login_required
def delete(contact_id):
    contact = Contact.query.get_or_404(contact_id)
    contact.is_active = False
    db.session.commit()
    log_action('delete', 'contact', contact.id, contact.name)
    flash('연락처가 삭제되었습니다.', 'success')
    return redirect(url_for('contacts.index'))


@contacts_bp.route('/export')
@login_required
def export_csv():
    import pandas as pd
    contacts = Contact.query.filter_by(is_active=True).order_by(Contact.name).all()
    rows = [c.to_dict() for c in contacts]
    for r in rows:
        r['categories'] = ', '.join(r['categories'])
        r['tags'] = ', '.join(r['tags'])

    df = pd.DataFrame(rows)
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Contacts')
    output.seek(0)
    log_action('export', 'contact', description='Exported all contacts')
    return send_file(output,
                     download_name='contacts.xlsx',
                     as_attachment=True,
                     mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')


@contacts_bp.route('/import', methods=['GET', 'POST'])
@login_required
def import_contacts():
    form = ImportForm()
    if form.validate_on_submit():
        f = form.file.data
        ext = os.path.splitext(f.filename)[1].lower()
        filename = f'{uuid.uuid4().hex}{ext}'
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        f.save(filepath)

        try:
            rows = parse_import_file(filepath)
            count = 0
            for row in rows:
                mapped = {COLUMN_MAP[k]: v for k, v in row.items() if k in COLUMN_MAP and v}
                if not mapped.get('name'):
                    continue
                contact = Contact(created_by=current_user.id, **mapped)
                db.session.add(contact)
                count += 1
            db.session.commit()
            log_action('import', 'contact', description=f'Imported {count} contacts')
            flash(f'{count}개의 연락처를 가져왔습니다.', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'파일 처리 중 오류가 발생했습니다: {str(e)}', 'danger')
        finally:
            os.remove(filepath)

        return redirect(url_for('contacts.index'))
    return render_template('contacts/import.html', form=form)

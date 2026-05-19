import io
import json
from flask import Blueprint, render_template, redirect, url_for, flash, request, send_file
from flask_login import login_required
from app import db
from app.models.user import User
from app.models.contact import Contact
from app.models.category import Category
from app.models.tag import Tag
from app.models.audit_log import AuditLog
from app.forms.admin import CategoryForm, TagForm, UserEditForm
from app.utils import admin_required, log_action

admin_bp = Blueprint('admin', __name__)


@admin_bp.before_request
@login_required
def require_admin():
    from flask_login import current_user
    from flask import abort
    if not current_user.is_admin:
        abort(403)


# ── 대시보드 ────────────────────────────────────────────────
@admin_bp.route('/')
def dashboard():
    stats = {
        'users': User.query.count(),
        'contacts': Contact.query.filter_by(is_active=True).count(),
        'categories': Category.query.count(),
        'tags': Tag.query.count(),
    }
    recent_logs = AuditLog.query.order_by(AuditLog.created_at.desc()).limit(20).all()
    return render_template('admin/dashboard.html', stats=stats, recent_logs=recent_logs)


# ── 사용자 관리 ────────────────────────────────────────────
@admin_bp.route('/users')
def users():
    users = User.query.order_by(User.created_at.desc()).all()
    return render_template('admin/users.html', users=users)


@admin_bp.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    form = UserEditForm(obj=user)
    if form.validate_on_submit():
        user.role = form.role.data
        user.is_active = form.is_active.data
        db.session.commit()
        log_action('update', 'user', user.id, f'Role={user.role}')
        flash('사용자 정보가 수정되었습니다.', 'success')
        return redirect(url_for('admin.users'))
    return render_template('admin/user_edit.html', form=form, user=user)


# ── 카테고리 관리 ──────────────────────────────────────────
@admin_bp.route('/categories')
def categories():
    categories = Category.query.order_by('name').all()
    form = CategoryForm()
    return render_template('admin/categories.html', categories=categories, form=form)


@admin_bp.route('/categories/new', methods=['POST'])
def create_category():
    form = CategoryForm()
    if form.validate_on_submit():
        cat = Category(name=form.name.data, description=form.description.data, color=form.color.data)
        db.session.add(cat)
        db.session.commit()
        log_action('create', 'category', cat.id, cat.name)
        flash('카테고리가 추가되었습니다.', 'success')
    return redirect(url_for('admin.categories'))


@admin_bp.route('/categories/<int:cat_id>/delete', methods=['POST'])
def delete_category(cat_id):
    cat = Category.query.get_or_404(cat_id)
    db.session.delete(cat)
    db.session.commit()
    log_action('delete', 'category', cat_id, cat.name)
    flash('카테고리가 삭제되었습니다.', 'success')
    return redirect(url_for('admin.categories'))


# ── 태그 관리 ──────────────────────────────────────────────
@admin_bp.route('/tags')
def tags():
    tags = Tag.query.order_by('name').all()
    form = TagForm()
    return render_template('admin/tags.html', tags=tags, form=form)


@admin_bp.route('/tags/new', methods=['POST'])
def create_tag():
    form = TagForm()
    if form.validate_on_submit():
        tag = Tag(name=form.name.data, color=form.color.data)
        db.session.add(tag)
        db.session.commit()
        log_action('create', 'tag', tag.id, tag.name)
        flash('태그가 추가되었습니다.', 'success')
    return redirect(url_for('admin.tags'))


@admin_bp.route('/tags/<int:tag_id>/delete', methods=['POST'])
def delete_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()
    log_action('delete', 'tag', tag_id, tag.name)
    flash('태그가 삭제되었습니다.', 'success')
    return redirect(url_for('admin.tags'))


# ── 감사 로그 ──────────────────────────────────────────────
@admin_bp.route('/logs')
def logs():
    page = request.args.get('page', 1, type=int)
    pagination = AuditLog.query.order_by(AuditLog.created_at.desc()).paginate(
        page=page, per_page=50, error_out=False)
    return render_template('admin/logs.html', pagination=pagination)


# ── 백업/복원 ──────────────────────────────────────────────
@admin_bp.route('/backup')
def backup():
    contacts = [c.to_dict() for c in Contact.query.filter_by(is_active=True).all()]
    payload = json.dumps({'contacts': contacts}, ensure_ascii=False, default=str)
    buf = io.BytesIO(payload.encode('utf-8'))
    log_action('backup', description='Full backup')
    return send_file(buf, download_name='phonebook_backup.json',
                     as_attachment=True, mimetype='application/json')


@admin_bp.route('/restore', methods=['POST'])
def restore():
    from app.models.contact import Contact as C
    f = request.files.get('backup_file')
    if not f:
        flash('파일을 선택해주세요.', 'warning')
        return redirect(url_for('admin.dashboard'))
    try:
        data = json.load(f)
        count = 0
        from flask_login import current_user
        for row in data.get('contacts', []):
            row.pop('id', None)
            row.pop('categories', None)
            row.pop('tags', None)
            row.pop('created_at', None)
            contact = C(created_by=current_user.id, **{k: v for k, v in row.items() if hasattr(C, k)})
            db.session.add(contact)
            count += 1
        db.session.commit()
        log_action('restore', description=f'Restored {count} contacts')
        flash(f'{count}개 연락처를 복원했습니다.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'복원 중 오류: {str(e)}', 'danger')
    return redirect(url_for('admin.dashboard'))

from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models.user import User
from app.forms.auth import LoginForm, RegisterForm, ChangePasswordForm
from app.utils import log_action

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('contacts.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data) and user.is_active:
            login_user(user, remember=form.remember_me.data)
            user.last_login = datetime.utcnow()
            db.session.commit()
            log_action('login', description=f'User {user.email} logged in')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('contacts.index'))
        flash('이메일 또는 비밀번호가 올바르지 않습니다.', 'danger')
    return render_template('auth/login.html', form=form)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('contacts.index'))
    form = RegisterForm()
    if form.validate_on_submit():
        is_first = User.query.count() == 0
        user = User(
            username=form.username.data,
            email=form.email.data,
            role='admin' if is_first else 'user',
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        log_action('register', 'user', user.id, f'New user {user.email}')
        flash('계정이 생성되었습니다. 로그인하세요.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    log_action('logout', description=f'User {current_user.email} logged out')
    logout_user()
    flash('로그아웃되었습니다.', 'info')
    return redirect(url_for('auth.login'))


@auth_bp.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.check_password(form.old_password.data):
            current_user.set_password(form.new_password.data)
            db.session.commit()
            log_action('change_password', 'user', current_user.id)
            flash('비밀번호가 변경되었습니다.', 'success')
            return redirect(url_for('contacts.index'))
        flash('현재 비밀번호가 올바르지 않습니다.', 'danger')
    return render_template('auth/change_password.html', form=form)

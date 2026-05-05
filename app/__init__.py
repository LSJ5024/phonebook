from flask import Flask, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_babel import Babel
from flask_mail import Mail
from config.config import config

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
csrf = CSRFProtect()
babel = Babel()
mail = Mail()

login_manager.login_view = 'auth.login'
login_manager.login_message = '이 페이지에 접근하려면 로그인이 필요합니다.'
login_manager.login_message_category = 'warning'


def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)
    mail.init_app(app)

    def get_locale():
        lang = session.get('lang')
        if lang in app.config['BABEL_SUPPORTED_LOCALES']:
            return lang
        return request.accept_languages.best_match(app.config['BABEL_SUPPORTED_LOCALES'], 'ko')

    babel.init_app(app, locale_selector=get_locale)

    from app.views.auth import auth_bp
    from app.views.contacts import contacts_bp
    from app.views.admin import admin_bp
    from app.views.api import api_bp
    from app.views.main import main_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(contacts_bp, url_prefix='/contacts')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(api_bp, url_prefix='/api/v1')

    from app.views import errors
    app.register_error_handler(404, errors.not_found)
    app.register_error_handler(403, errors.forbidden)
    app.register_error_handler(500, errors.internal_error)

    import os
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    return app


from app.models.user import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

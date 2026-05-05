from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from app.models.user import User


class LoginForm(FlaskForm):
    email = StringField('이메일', validators=[DataRequired(), Email()])
    password = PasswordField('비밀번호', validators=[DataRequired()])
    remember_me = BooleanField('로그인 상태 유지')
    submit = SubmitField('로그인')


class RegisterForm(FlaskForm):
    username = StringField('사용자명', validators=[DataRequired(), Length(2, 64)])
    email = StringField('이메일', validators=[DataRequired(), Email()])
    password = PasswordField('비밀번호', validators=[DataRequired(), Length(8, 128)])
    password2 = PasswordField('비밀번호 확인', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('회원가입')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('이미 사용 중인 사용자명입니다.')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('이미 등록된 이메일입니다.')


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('현재 비밀번호', validators=[DataRequired()])
    new_password = PasswordField('새 비밀번호', validators=[DataRequired(), Length(8, 128)])
    new_password2 = PasswordField('새 비밀번호 확인', validators=[DataRequired(), EqualTo('new_password')])
    submit = SubmitField('변경')


class ResetPasswordRequestForm(FlaskForm):
    email = StringField('이메일', validators=[DataRequired(), Email()])
    submit = SubmitField('재설정 링크 전송')

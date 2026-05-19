from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Optional


class CategoryForm(FlaskForm):
    name = StringField('카테고리명', validators=[DataRequired(), Length(1, 100)])
    description = StringField('설명', validators=[Optional(), Length(max=255)])
    color = StringField('색상', default='#007BFF')
    submit = SubmitField('저장')


class TagForm(FlaskForm):
    name = StringField('태그명', validators=[DataRequired(), Length(1, 50)])
    color = StringField('색상', default='#6C757D')
    submit = SubmitField('저장')


class UserEditForm(FlaskForm):
    role = SelectField('권한', choices=[('user', '일반 사용자'), ('admin', '관리자')])
    is_active = BooleanField('활성 계정')
    submit = SubmitField('저장')

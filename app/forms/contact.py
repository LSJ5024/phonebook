from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, SelectMultipleField, SubmitField
from wtforms.validators import Optional, Email, Length


class ContactForm(FlaskForm):
    name = StringField('이름', validators=[Length(1, 100)])
    phone = StringField('전화번호', validators=[Optional(), Length(max=30)])
    mobile = StringField('휴대폰', validators=[Optional(), Length(max=30)])
    email = StringField('이메일', validators=[Optional(), Email(), Length(max=120)])
    organization = StringField('소속', validators=[Optional(), Length(max=150)])
    department = StringField('부서', validators=[Optional(), Length(max=100)])
    position = StringField('직책', validators=[Optional(), Length(max=100)])
    address = StringField('주소', validators=[Optional(), Length(max=255)])
    memo = TextAreaField('메모', validators=[Optional()])
    categories = SelectMultipleField('카테고리', coerce=int, validators=[Optional()])
    tags = SelectMultipleField('태그', coerce=int, validators=[Optional()])
    submit = SubmitField('저장')


class ContactSearchForm(FlaskForm):
    class Meta:
        csrf = False

    q = StringField('검색어', validators=[Optional()])
    category = SelectMultipleField('카테고리', coerce=int, validators=[Optional()])
    tag = SelectMultipleField('태그', coerce=int, validators=[Optional()])


class ImportForm(FlaskForm):
    file = FileField('파일 선택', validators=[
        FileAllowed(['csv', 'xlsx', 'xls'], 'CSV 또는 Excel 파일만 업로드 가능합니다.')
    ])
    submit = SubmitField('가져오기')

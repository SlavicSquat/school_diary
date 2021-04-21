from flask_wtf import FlaskForm
from wtforms import FieldList, FormField, BooleanField, RadioField
from wtforms.validators import DataRequired
from wtforms import SubmitField


class RegTeach(FlaskForm):
    checkmath = BooleanField('Математика')
    checkrus = BooleanField('Русский язык')
    checkphys = BooleanField('Физика')


class RegStudent(FlaskForm):
    radioclass = RadioField('aboba', choices=[('5А', '5А'), ('5Б', '5Б'), ('6А', '6А')], validators=[DataRequired()])


class TSub(FlaskForm):
    sub_info = FieldList(FormField(RegTeach), min_entries=1, label='Какие предметы вы ведёте?')
    submit = SubmitField('Регистрация')


class SSub(FlaskForm):
    sub_info = FieldList(FormField(RegStudent), min_entries=1, label='В каком классе вы учитесь?')
    submit = SubmitField('Регистрация')

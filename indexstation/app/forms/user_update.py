from flask_wtf import FlaskForm
from wtforms import SubmitField, PasswordField
from wtforms.validators import DataRequired, EqualTo, ValidationError
from app import models
from flask_login import current_user

class PasswordUpdateForm(FlaskForm):
        def validate_old_password(self, password_old):
        if not current_user.check_password(password_old.data):
                raise ValidationError('Старый пароль введен неправильно')

        def validate_new_password(self, password_new1):
        if current_user.check_password(password_new1.data):
                raise ValidationError('Новый и старый пороли совпадают')

    password_old = PasswordField('Старый пароль', validators=[DataRequired(), self.validate_old_password])
    password_new1 = PasswordField('Новый пароль', validators=[DataRequired(), self.validate_new_password])
    password_new2 = PasswordField('Подтвердите пароль', validators=[DataRequired(), EqualTo('password_new1', message='Пароли должны совпадать')])
    submit = SubmitField('Изменить')К
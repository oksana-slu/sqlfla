from flask.ext.wtf import Form, TextField, PasswordField, validators


class AuthForm(Form):
    login = TextField(description='Login', validators=[validators.Email(),
                                                       validators.Required()])
    password = PasswordField(description='Password',
                             validators=[validators.Required()])

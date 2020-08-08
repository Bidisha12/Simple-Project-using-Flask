from wtforms import Form, TextField, PasswordField, RadioField, SelectField, TextAreaField, validators

class LoginForm(Form):
    username = TextField('Username', [validators.Email('Please enter your valid email')])
    password = PasswordField('Password', [validators.Length(min=6, max=15, message='Password should be 6 to 15 characters')])

class RegisterForm(Form):
    name = TextField('Name', [validators.Required()])
    email = TextField('Email', [validators.Email('Please enter valid email')])
    password = PasswordField('Password', [validators.Length(min=6, max=15, message='Password must be 6 to 15 characters')])
    #('C','C') = ('Value','Label')
    gender = RadioField('Gender', [validators.Required()], choices=[('Male','Male'),('Female','Female')])
    prolanguage = SelectField('Language', [validators.Required()], choices=[('','-Select-'),('C','C'),('CPP','C++'),('Java','Java'),('Python','Python')])

class EmployeeForm(Form):
    firstname = TextField('Firstname', [validators.Required()])
    midname = TextField('Middlename', [validators.Optional()])
    lastname = TextField('Lastname', [validators.Required()])
    address = TextAreaField('Address', [validators.Required()])
    email = TextField('Email', [validators.Email('Please enter valid email')])
    mobile = TextField('Mobile', [validators.Length(min=10, max=10, message='Mobile no. must be 10 digits')])
    gender = RadioField('Gender', [validators.Required()], choices=[('Male','Male'),('Female','Female')])
    designation = SelectField('Designation', [validators.Required()], choices=[('','-Select Designation'),('Programmer','Programmer'),('Designer','Designer')])

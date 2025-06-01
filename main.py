from flask import Flask, render_template, request, flash, json
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email
from flask_wtf.recaptcha import RecaptchaField
from flask_mail import Mail, Message

app = Flask(__name__, template_folder="template")
app.config['SECRET_KEY'] = "abc"
app.config['RECAPTCHA_USE_SSL'] = False
app.config['RECAPTCHA_PUBLIC_KEY'] = "6LfZXFErAAAAAKoTSk4PK8eed2YwIndBeSuMOlbZ"
app.config['RECAPTCHA_PRIVATE_KEY'] = "6LfZXFErAAAAAJVYN_JS5-RnZScPQ1SY3FQNnn7x"
app.config['RECAPTCHA_OPTIONS'] = {'theme': 'black'}


# json file for data fetching
with open('config.json', 'r') as f:
    params = json.load(f)['parameters']
# config the mail setting
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = params['user-gmail']
app.config['MAIL_PASSWORD'] = params['app-password']
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
mail = Mail(app)


class ContactForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    comment = TextAreaField("Comment", validators=[DataRequired()])
    recaptcha = RecaptchaField()
    submit = SubmitField("Submit")



@app.route("/")
def home():
    form = ContactForm()
    return render_template("wtform.html", form=form)


@app.route("/info", methods=["POST"])
def info():
    form = ContactForm()

    if request.method == "POST" and form.validate():
        username = form.username.data
        email = form.email.data
        comment = form.comment.data

        # Send email
        msg = Message(
            subject="Text Me",
            sender=email,
            recipients=["fahadyt55678@gmail.com"]
        )
        msg.body = f"Username: {username}\nEmail: {email}\nComment: {comment}"
        mail.send(msg)

        flash("Message sent successfully!")

    return render_template("wtform.html", form=form)

if __name__ == '__main__':
    app.run(debug=True)

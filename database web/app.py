from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from send_email import send_email
from sqlalchemy.sql import func

app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:noanir12@localhost/height_collector'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://vfqgxkhfosiunf:ade96fab7ef9ca2f312b63749aeb50d12a581cc5ef9b2849b9f2f3b48038f7a3@ec2-34-233-226-84.compute-1.amazonaws.com:5432/d1ouor7q82us4a?sslmode=require'
db = SQLAlchemy(app)


class Data(db.Model):
    __tablename__ = "data"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    height = db.Column(db.Integer)

    def __init__(self, email_, height_):
        self.email = email_
        self.height = height_


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/success', methods=['POST'])
def success():
    if request.method == 'POST':
        email = request.form["email_name"]
        height = request.form["height_name"]
        if db.session.query(Data).filter(Data.email == email).count() == 0:
            data = Data(email, height)
            db.session.add(data)
            db.session.commit()
            avg_height = db.session.query(func.avg(Data.height)).scalar()
            avg_height = round(avg_height, 1)
            num_of_users = db.session.query(Data.height).count()
            send_email(email, height, avg_height, num_of_users)
            return render_template("success.html")
        else:
            return render_template("index.html",
                                   text="Seems like we've got something from this email address already")


if __name__ == "__main__":
    app.debug = True
    app.run(port=5001)

from flask import Flask, render_template,request,redirect,flash,session,logging, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import login_required,current_user
import os

project_dir=os.path.dirname(os.path.abspath(__file__))
database_file="sqlite:///{}".format(os.path.join(project_dir, "auctions.db"))

db=SQLAlchemy()

app = Flask(__name__)
#add after login business
app.config['SECRET_KEY'] = 'long secret key'
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
#add it all time to avoid warning
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/profile', methods=['GET'])
@login_required
def profil():
    return render_template('profile.html',name=current_user.name)




if __name__ == '__main__':
    app.run(debug=True)
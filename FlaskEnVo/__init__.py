from flask import Flask, render_template,request,redirect,flash,session,logging, url_for
from flask_sqlalchemy import SQLAlchemy
import os
from flask_login import LoginManager

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

@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(user_id)




if __name__ == '__main__':
    app.run(debug=True)
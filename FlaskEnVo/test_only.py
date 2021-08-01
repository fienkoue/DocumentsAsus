from flask import Flask, render_template,request,redirect,flash,session,logging, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from models import db,CarsModel,User,UserMixin,LoginManager,generate_password_hash,check_password_hash,current_user,LoginManager,login_user,logout_user,login_required
from forms import LoginForm, RegisterForm

project_dir=os.path.dirname(os.path.abspath(__file__))
database_file="sqlite:///{}".format(os.path.join(project_dir, "auctions.db"))

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = database_file
#add it all time to avoid warning
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)




@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        brand = request.form['brand']
        model = request.form['model']
        prices = request.form['prices']
        year = request.form['year']
        fuel = request.form['fuel']
        kms = request.form['kms']
        new_stuff = CarsModel(brand=brand,model=model,prices=prices,year=year,fuel=fuel,kms=kms)

        try:
            db.session.add(new_stuff)
            db.session.commit()
            return redirect('/')
        except:
            return "There was a problem adding new car."

    else:
        cars=CarsModel.query.all()
        return render_template('index.html', cars=cars)


#works but check except
@app.route('/car/<int:id>', methods=['GET'])
def RetrieveSingleCar(id):
    car = CarsModel.query.get_or_404(id)
    try:
        db.session.commit()
        return render_template('results.html',car=car)
    except:
        return f"vilenave with id={id} doesnt exist"

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    car = CarsModel.query.get_or_404(id)

    if request.method == 'POST':
        car.brand = request.form['brand']
        car.model = request.form['model']
        car.prices = request.form['prices']
        car.year = request.form['year']
        car.fuel = request.form['fuel']
        car.kms = request.form['kms']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return "There was a problem updating data."

    else:
        title = "Update Data"
        return render_template('update.html', title=title, car=car)

@app.route('/delete/<int:id>')
def delete(id):
    car = CarsModel.query.get_or_404(id)

    try:
        db.session.delete(car)
        db.session.commit()
        return redirect('/')
    except:
        return "There was a problem deleting data."



if __name__ == '__main__':
    app.run(debug=True)
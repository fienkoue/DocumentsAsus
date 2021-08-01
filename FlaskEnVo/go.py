from flask import Flask, render_template,request,redirect,flash,session,logging, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from models import db,CarsModel,User,UserMixin,generate_password_hash,check_password_hash,current_user,LoginManager,login_user,logout_user,login_required
from forms import LoginForm, RegisterForm

project_dir=os.path.dirname(os.path.abspath(__file__))
database_file="sqlite:///{}".format(os.path.join(project_dir, "auctions.db"))

app = Flask(__name__)
#add after login business
app.config['SECRET_KEY'] = 'long secret key'
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
#add it all time to avoid warning
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'


@app.route('/all', methods=['GET', 'POST'])
def getAll():
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
            return redirect('/all')
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
        return f"car with id={id} doesnt exist"

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

@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(user_id)

# User Registration Api End Point
@app.route('/register/', methods = ['GET', 'POST'])
def register():
    # Creating RegistrationForm class object
    form = RegisterForm(request.form)

    # Cheking that method is post and form is valid or not.
    if request.method == 'POST' and form.validate():

        # if all is fine, generate hashed password
        hashed_password = generate_password_hash(form.password.data, method='sha256')

        # create new user model object
        new_user = User(

            name = form.name.data, 

            username = form.username.data, 

            email = form.email.data, 

            password = hashed_password )

        # saving user object into data base with hashed password
        db.session.add(new_user)

        db.session.commit()

        flash('You have successfully registered', 'success')

        # if registration successful, then redirecting to login Api
        return redirect(url_for('login'))

    else:

        # if method is Get, than render registration form
        return render_template('register.html', form = form)

@app.route('/admin/')
@login_required
def admin():
    return render_template('admin.html')

@app.route('/login/', methods=['post', 'get'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin'))

    form = LoginForm(request.form)

    if request.method == 'POST' and form.validate:
        user = db.session.query(User).filter(User.username == form.username.data).first()

        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('admin'))

        flash("Invalid username/password", 'error')
        return redirect(url_for('login'))
    return render_template('login.html', form=form)

@app.route('/logout/')
@login_required
def logout():
    logout_user()    
    flash("You have been logged out.")
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
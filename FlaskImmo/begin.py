from flask import Flask, render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from models import db,VillenavModel

project_dir=os.path.dirname(os.path.abspath(__file__))
database_file="sqlite:///{}".format(os.path.join(project_dir, "immo.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
#add it all time to avoid warning
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        id_mutation = request.form['id_mutation']
        #convert date to correct format to avoid error sqlite date type only accept python date objects as input 
        date_mutation = datetime.strptime(request.form['date_mutation'],"%Y-%m-%d").date() 
        numero_disposition = request.form['numero_disposition']
        nature_mutation = request.form['nature_mutation']
        valeur_fonciere = request.form['valeur_fonciere']
        new_stuff = VillenavModel(id_mutation=id_mutation,date_mutation=date_mutation,numero_disposition=numero_disposition,nature_mutation=nature_mutation,valeur_fonciere=valeur_fonciere)

        try:
            db.session.add(new_stuff)
            db.session.commit()
            return redirect('/')
        except:
            return "There was a problem adding new stuff."

    else:
        vilenaves=VillenavModel.query.all()
        return render_template('index.html', vilenaves=vilenaves)

#works but check except
@app.route('/vilenave/<int:id>', methods=['GET'])
def RetrieveSingleVilenave(id):
    vilenave = VillenavModel.query.get_or_404(id)
    try:
        db.session.commit()
        return render_template('results.html',vilenave=vilenave)
    except:
        return f"vilenave with id={id} doesnt exist"


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    vilenave = VillenavModel.query.get_or_404(id)

    if request.method == 'POST':
        vilenave.id_mutation = request.form['id_mutation']
        #convert date to correct format to avoid error sqlite date type only accept python date objects as input 
        vilenave.date_mutation = datetime.strptime(request.form['date_mutation'],"%Y-%m-%d").date() 
        vilenave.numero_disposition = request.form['numero_disposition']
        vilenave.nature_mutation = request.form['nature_mutation']
        vilenave.valeur_fonciere = request.form['valeur_fonciere']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return "There was a problem updating data."

    else:
        title = "Update Data"
        return render_template('update.html', title=title, vilenave=vilenave)

@app.route('/delete/<int:id>')
def delete(id):
    vilenave = VillenavModel.query.get_or_404(id)

    try:
        db.session.delete(vilenave)
        db.session.commit()
        return redirect('/')
    except:
        return "There was a problem deleting data."




if __name__ == '__main__':
    app.run(debug=True)




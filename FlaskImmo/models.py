from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

class VillenavModel(db.Model):
    __tablename__="vilenave"

    id=db.Column(db.Integer,primary_key=True)
    id_mutation=db.Column(db.String(50))
    #Put date here and not DateTime because format of date results looks like simple date e.g : 2020-04-02 to avoid couldnt parse datetime string python sqlite value error
    date_mutation = db.Column(db.Date)
    numero_disposition = db.Column(db.Integer)
    nature_mutation =db.Column(db.String(50))
    valeur_fonciere =db.Column(db.Float)


    def __init__(self,id_mutation,date_mutation,numero_disposition,nature_mutation,valeur_fonciere):
        self.id_mutation=id_mutation
        self.date_mutation=date_mutation
        self.numero_disposition=numero_disposition
        self.nature_mutation=nature_mutation
        self.valeur_fonciere=valeur_fonciere

    def __repr__(self):
        return f"{self.nature_mutation}:{self.valeur_fonciere}"


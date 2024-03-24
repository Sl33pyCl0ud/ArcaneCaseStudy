from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

# Obtenez le chemin absolu du répertoire courant
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
# Utilisez un chemin relatif pour la base de données SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'Sqlite', 'ArcaneCaseStudyDatabase.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class biens_immobiliers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    type_de_bien = db.Column(db.String(50), nullable=False)
    ville = db.Column(db.String(50), nullable=False)
    pieces = db.Column(db.Integer, nullable=False)
    caracteristiques_pieces = db.Column(db.Text, nullable=True)
    proprietaire_id = db.Column(db.Integer, db.ForeignKey('utilisateurs.id'), nullable=False)


class utilisateurs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(50), nullable=False)
    prenom = db.Column(db.String(50), nullable=False)
    date_de_naissance = db.Column(db.Date, nullable=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    mot_de_passe = db.Column(db.String(100), nullable=False)
    ville = db.Column(db.String(50), nullable=True)


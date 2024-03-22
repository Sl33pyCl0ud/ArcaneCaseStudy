from flask import request, jsonify, g
from app import app, db, biens_immobiliers, utilisateurs as u

# Routes pour les biens immobiliers

@app.route('/biens_immobiliers', methods=['GET'])
def get_biens_immobiliers():
    biens_immobiliers = biens_immobiliers.query.all()
    result = [{"id": bien.id, "nom": bien.nom, "description": bien.description, "type_de_bien": bien.type_de_bien, "ville": bien.ville, "pieces": bien.pieces, "caracteristiques_pieces": bien.caracteristiques_pieces, "proprietaire_id": bien.proprietaire_id} for bien in biens_immobiliers]
    return jsonify({"biens_immobiliers": result}), 200

@app.route('/biens_immobiliers/<int:bien_id>', methods=['GET'])
def get_bien_immobilier(bien_id):
    bien = biens_immobiliers.query.get_or_404(bien_id)
    return jsonify({"id": bien.id, "nom": bien.nom, "description": bien.description, "type_de_bien": bien.type_de_bien, "ville": bien.ville, "pieces": bien.pieces, "caracteristiques_pieces": bien.caracteristiques_pieces, "proprietaire_id": bien.proprietaire_id}), 200

@app.route('/biens_immobiliers/ville/<ville>', methods=['GET'])
def get_biens_immobiliers_par_ville(ville):
    biens_immobiliers = biens_immobiliers.query.filter_by(ville=ville).all()
    result = [{"id": bien.id, "nom": bien.nom, "description": bien.description, "type_de_bien": bien.type_de_bien, "ville": bien.ville, "pieces": bien.pieces, "caracteristiques_pieces": bien.caracteristiques_pieces, "proprietaire_id": bien.proprietaire_id} for bien in biens_immobiliers]
    return jsonify({"biens_immobiliers": result}), 200

@app.route('/biens_immobiliers', methods=['POST'])
def create_bien_immobilier():
    data = request.get_json()
    nouveau_bien = biens_immobiliers(nom=data['nom'], description=data['description'], type_de_bien=data['type_de_bien'], ville=data['ville'], pieces=data['pieces'], caracteristiques_pieces=data['caracteristiques_pieces'], proprietaire_id=data['proprietaire_id'])
    db.session.add(nouveau_bien)
    db.session.commit()
    return jsonify({"message": "Nouveau bien immobilier créé"}), 201

@app.route('/biens_immobiliers/<int:bien_id>', methods=['PUT'])
def update_bien_immobilier(bien_id):
    # Récupérer le bien immobilier à mettre à jour depuis la base de données
    bien_immobilier = biens_immobiliers.query.get_or_404(bien_id)
    
    # Vérifier si l'utilisateur est authentifié
    if g.user is None:
        return jsonify({"message": "utilisateurs non authentifié"}), 401
    
    # Vérifier si l'utilisateur est le propriétaire du bien immobilier
    if bien_immobilier.proprietaire_id != g.user.id:
        return jsonify({"message": "Vous n'êtes pas autorisé à modifier ce bien immobilier"}), 403
    
    # Logique pour mettre à jour le bien immobilier
    data = request.get_json()
    bien_immobilier.nom = data['nom']
    bien_immobilier.description = data['description']
    bien_immobilier.type_de_bien = data['type_de_bien']
    bien_immobilier.ville = data['ville']
    bien_immobilier.pieces = data['pieces']
    bien_immobilier.caracteristiques_pieces = data['caracteristiques_pieces']
    db.session.commit()
    
    return jsonify({"message": f"Le bien immobilier {bien_id} a été mis à jour"}), 200


@app.route('/biens_immobiliers/<int:bien_id>', methods=['DELETE'])
def delete_bien_immobilier(bien_id):
    bien = biens_immobiliers.query.get_or_404(bien_id)
    db.session.delete(bien)
    db.session.commit()
    return jsonify({"message": f"Le bien immobilier {bien_id} a été supprimé"}), 200

# Routes pour les utilisateurs

@app.route('/utilisateurs', methods=['GET'])
def get_utilisateurs():
    utilisateurs = u.query.all()
    result = [{"id": utilisateur.id, "nom": utilisateur.nom, "prenom": utilisateur.prenom, "date_de_naissance": utilisateur.date_de_naissance, "email": utilisateur.email, "ville": utilisateur.ville} for utilisateur in utilisateurs]
    return jsonify({"utilisateurs": result}), 200

@app.route('/utilisateurs/<int:utilisateur_id>', methods=['GET'])
def get_utilisateur(utilisateur_id):
    utilisateur = u.query.get_or_404(utilisateur_id)
    return jsonify({"id": utilisateur.id, "nom": utilisateur.nom, "prenom": utilisateur.prenom, "date_de_naissance": utilisateur.date_de_naissance, "email": utilisateur.email, "ville": utilisateur.ville}), 200

@app.route('/utilisateurs', methods=['POST'])
def create_utilisateur():
    data = request.get_json()
    nouvel_utilisateur = u(nom=data['nom'], prenom=data['prenom'], date_de_naissance=data['date_de_naissance'], email=data['email'], mot_de_passe=data['mot_de_passe'], ville=data['ville'])
    db.session.add(nouvel_utilisateur)
    db.session.commit()
    return jsonify({"message": "Nouvel utilisateur créé"}), 201

@app.route('/utilisateurs/<int:utilisateur_id>', methods=['PUT'])
def update_utilisateur(utilisateur_id):
    utilisateur = u.query.get_or_404(utilisateur_id)
    data = request.get_json()
    utilisateur.nom = data['nom']
    utilisateur.prenom = data['prenom']
    utilisateur.date_de_naissance = data['date_de_naissance']
    utilisateur.email = data['email']
    utilisateur.ville = data['ville']
    db.session.commit()
    return jsonify({"message": f"L'utilisateur {utilisateur_id} a été mis à jour"}), 200

@app.route('/utilisateurs/<int:utilisateur_id>', methods=['DELETE'])
def delete_utilisateur(utilisateur_id):
    utilisateur = u.query.get_or_404(utilisateur_id)
    db.session.delete(utilisateur)
    db.session.commit()
    return jsonify({"message": f"L'utilisateur {utilisateur_id} a été supprimé"}), 200

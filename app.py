from flask import Flask, request, jsonify, send_from_directory
from pymongo import MongoClient
from bson import ObjectId, json_util
import json

app = Flask(__name__)

# Connexion à MongoDB
client = MongoClient("mongodb+srv://haaahiii:1234@cluster1.wmj7n.mongodb.net/?retryWrites=true&w=majority&appName=Cluster1")
db = client['Data_ko']
collection = db['Data_collectio_nama']

@app.route('/')
def serve_frontend():
    return send_from_directory('templates', 'index.html')

@app.route('/create', methods=['POST'])
def create_data():
    data = request.json
    result = collection.insert_one(data)
    return jsonify({"status": "success", "inserted_id": str(result.inserted_id)})

@app.route('/get_data', methods=['GET'])
def get_data():
    data = list(collection.find())
    json_data = json.loads(json_util.dumps(data))
    return jsonify(json_data)

@app.route('/update/<id>', methods=['PUT'])
def update_data(id):
    data = request.json
    result = collection.update_one({"_id": ObjectId(id)}, {"$set": data})
    return jsonify({"status": "success", "modified_count": result.modified_count})

@app.route('/delete/<id>', methods=['DELETE'])
def delete_data(id):
    result = collection.delete_one({"_id": ObjectId(id)})
    return jsonify({"status": "success", "deleted_count": result.deleted_count})

@app.route('/authenticate', methods=['POST'])
def authenticate():
    # Exemple d'authentification simple
    data = request.get_json()
    carte = data.get("Carte")

    # Rechercher la carte dans la collection MongoDB
    user = collection.find_one({"Carte": carte})
    
    if user:
        # Construire la réponse avec l'_id inclus
        response = {
            "authenticated": True,
            "Nom": user.get("Nom", ""),
            "Carte": user.get("Carte", ""),
            "Compte": user.get("Compte", ""),
            "_id": {"$oid": str(user["_id"])}  # Convertir ObjectId en chaîne
        }
    else:
        response = {"authenticated": False}

    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

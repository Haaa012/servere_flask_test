from flask import Flask, jsonify
from pymongo import MongoClient
from bson import json_util
import json
app = Flask(__name__)
# Connexion à MongoDB
client = MongoClient("mongodb+srv://haaahiii:1234@cluster1.wmj7n.mongodb.net/?retryWrites=true&w=majority&appName=Cluster1")
db = client['Data_ko']
collection = db['Data_collectio_nama']
@app.route('/get_data')
def get_data():
    # Récupérer les données de MongoDB
    data = list(collection.find())
    # Convertir les données en JSON
    json_data = json.loads(json_util.dumps(data))    
    # Renvoyer les données au format JSON
    return jsonify(json_data)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

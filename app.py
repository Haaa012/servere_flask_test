from flask import Flask, request, jsonify, send_from_directory,render_template
from pymongo import MongoClient
from bson import ObjectId, json_util
from googletrans import Translator, LANGUAGES
import json

app = Flask(__name__)
translator = Translator()
# Connexion à MongoDB
client = MongoClient("mongodb+srv://haaahiii:1234@cluster1.wmj7n.mongodb.net/?retryWrites=true&w=majority&appName=Cluster1")
db = client['Data_ko']
collection = db['Data_collectio_nama']
# Associer les langues à leur code pays pour les drapeaux
country_flags = {
    'af': 'za',  # Afrikaans
    'sq': 'al',  # Albanian
    'am': 'et',  # Amharic
    'ar': 'ae',  # Arabic
    'hy': 'am',  # Armenian
    'az': 'az',  # Azerbaijani
    'eu': 'es',  # Basque
    'be': 'by',  # Belarusian
    'bn': 'bd',  # Bengali
    'bs': 'ba',  # Bosnian
    'bg': 'bg',  # Bulgarian
    'ca': 'es',  # Catalan
    'ceb': 'ph',  # Cebuano
    'ny': 'mw',  # Chichewa
    'zh-cn': 'cn', # Chinese (Simplified)
    'zh-tw': 'tw', # Chinese (Traditional)
    'co': 'fr',  # Corsican
    'hr': 'hr',  # Croatian
    'cs': 'cz',  # Czech
    'da': 'dk',  # Danish
    'nl': 'nl',  # Dutch
    'en': 'gb',  # English
    'eo': 'us',  # Esperanto
    'et': 'ee',  # Estonian
    'tl': 'ph',  # Filipino
    'fi': 'fi',  # Finnish
    'fr': 'fr',  # French
    'fy': 'nl',  # Frisian (Pays-Bas)
    'gl': 'es',  # Galician (Espagne)
    'ka': 'ge',  # Georgian (Géorgie)
    'de': 'de',  # German
    'el': 'gr',  # Greek
    'gu': 'in',  # Gujarati
    'ht': 'ht',  # Haitian creole (Haïti)
    'ha': 'ng',  # Hausa (Nigeria)
    'haw': 'us',  # Hawaiian (États-Unis)
    'he': 'il',  # Hebrew (Israël)
    'ku': 'tr',  # Kurdish (Kurmanji) (Turquie)
    'ky': 'kg',  # Kyrgyz (Kirghizistan)
    'lo': 'la',  # Lao (Laos)
    'hi': 'in',  # Hindi
    'hmn': 'vn',  # Hmong (Vietnam)
    'hu': 'hu',  # Hungarian
    'is': 'is',  # Icelandic
     'ig': 'ng',  # Igbo (Nigeria)
    'id': 'id',  # Indonesian
    'ga': 'ie',  # Irish (Irlande)
    'it': 'it',  # Italian
    'ja': 'jp',  # Japanese
    'jv': 'jv',  # Javanese (Indonésie)
    'kn': 'in',  # Kannada (Inde)
    'kk': 'kz',  # Kazakh (Kazakhstan)
    'km': 'kh',  # Khmer
    'ko': 'kr',  # Korean
    'la': 'la',  # Latin
    'lv': 'lv',  # Latvian
    'lt': 'lt',  # Lithuanian
    'mk': 'mk',  # Macedonian
    'mg': 'mg',  # Malagasy → Madagascar
    'ml': 'in',  # Malayalam
    'mt': 'mt',  # Maltese (Malte)
    'mi': 'nz',  # Maori (Nouvelle-Zélande)
    'mr': 'in',  # Marathi
    'mn': 'mn',  # Mongolian (Mongolie)
    'my': 'mm',  # Burmese (Myanmar)
    'ne': 'np',  # Nepali
    'no': 'no',  # Norwegian
    'pl': 'pl',  # Polish
    'ps': 'af',  # Pashto (Afghanistan)
    'pt': 'pt',  # Portuguese
    'pa': 'in',  # Punjabi (Inde)
    'ro': 'ro',  # Romanian
    'ru': 'ru',  # Russian
    'sr': 'rs',  # Serbian
    'si': 'lk',  # Sinhala
    'sk': 'sk',  # Slovak
    'sl': 'si',  # Slovenian
    'es': 'es',  # Spanish
    'su': 'id',  # Sundanese (Indonésie)
    'sw': 'ke',  # Swahili
    'sv': 'se',  # Swedish
    'tg': 'tj',  # Tajik (Tadjikistan)
    'ta': 'in',  # Tamil
    'te': 'in',  # Telugu
    'th': 'th',  # Thai (Thaïlande)
    'tr': 'tr',  # Turkish
    'uk': 'ua',  # Ukrainian
    'ur': 'pk',  # Urdu
    'ug': 'cn',  # Uyghur (Chine)
    'yo': 'ng',  # Yoruba (Nigeria)
    'vi': 'vn',  # Vietnamese
    'cy': 'gb',  # Welsh
    'xh': 'za',  # Xhosa
    'yi': 'il',  # Yiddish
    'zu': 'za',  # Zulu
    'he': 'il',  # Hebrew
    'sm': 'ws',  # Samoan
    'gd': 'gb',  # Scots Gaelic
    'st': 'za',  # Sesotho
    'sn': 'zw',  # Shona
    'so': 'so',  # Somali
    'fa': 'ir',  # Persian
    'or': 'in',  # Odia
    'lb': 'lu',  # Luxembourgish
    'uz': 'uz',  # Uzbek
}
@app.route('/')
def serve_frontend():
    return send_from_directory('templates', 'index.html')
@app.route('/listeclient')
def listeclient():
    return send_from_directory('templates', 'listeclient.html')    
@app.route("/traduction", methods=["GET", "POST"])
def traduction():
    translated_text = ""
    if request.method == "POST":
        text = request.form["text"]
        source_lang = request.form["source_lang"]
        target_lang = request.form["target_lang"]
        
        if text:
            translated_text = translator.translate(text, src=source_lang, dest=target_lang).text

    return render_template("traduction.html", translated_text=translated_text, languages=LANGUAGES, flags=country_flags)

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
    
@app.route('/authenticate_apk', methods=['POST'])
def authenticate_apk():
    # Récupérer les données envoyées dans la requête JSON
    data = request.get_json()
    nom = data.get("Nom")
    code = data.get("Code")
    phone = data.get("Phone")
    
    # Vérifier si les champs nom et code sont présents
    if not nom or not code or not phone:
        return jsonify({"authenticated": False, "message": "Nom ou code manquants"}), 400

    # Rechercher l'utilisateur par nom et code
    user = collection.find_one({"Nom": nom, "Code": code})

    if user:
        # L'utilisateur est authentifié
        response = {
            "authenticated": True,
            "Nom": user.get("Nom", ""),
            "Phone": user.get("Phone", ""),
            "Carte": user.get("Carte", ""),
            "Compte": user.get("Compte", ""),
            "_id": {"$oid": str(user["_id"])}  # Convertir l'ObjectId en chaîne
        }
    else:
        # Si l'utilisateur n'est pas trouvé avec le nom et le code
        response = {"authenticated": False, "message": "Nom ou code incorrect"}

    return jsonify(response)
@app.route('/authenticate', methods=['POST'])
def authenticate():
    # Exemple d'authentification simple
    data = request.get_json()
    carte = data.get("Carte")
    emprint = data.get("Idenprinte")

    # Rechercher la carte dans la collection MongoDB
    user = collection.find_one({"Carte": carte,"Idenprinte":emprint})
    
    if user:
        # Construire la réponse avec l'_id inclus
        response = {
            "authenticated": True,
            "Nom": user.get("Nom", ""),
            "Carte": user.get("Carte", ""),
            "Compte": user.get("Compte", ""),
            "Idemprinte": user.get("Idenprinte", ""),
            "_id": {"$oid": str(user["_id"])}  # Convertir ObjectId en chaîne
        }
    else:
        response = {"authenticated": False}

    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

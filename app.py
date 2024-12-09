from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def hello():
    return "Bonjour! Cette application est déployée sur Render."

if __name__ == '__main__':
    # Utilisez le port fourni par l'environnement ou 5000 par défaut
    port = int(os.environ.get('PORT', 5000))
    # Assurez-vous que l'application écoute sur '0.0.0.0' pour Render
    app.run(host='0.0.0.0', port=port)

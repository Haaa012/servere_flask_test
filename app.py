from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return "Bonjour! Cette application est déployée sur Render."

if __name__ == '__main__':
    app.run()

# Importation des modules nécessaires
from flask import Flask, render_template
from flask_socketio import SocketIO, send

users_online = 0

# Création de l'application Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'  # Clé secrète pour sécuriser les sessions

# Initialisation de SocketIO pour gérer les messages en temps réel
socketio = SocketIO(app)

@socketio.on('connect')
def handle_connect():
    global users_online
    users_online += 1
    socketio.emit('user_count', users_online)

@socketio.on('disconnect')
def handle_disconnect():
    global users_online
    users_online -= 1
    socketio.emit('user_count', users_online)

# Route principale : quand on va sur http://localhost:5000/
@app.route('/')
def index():
    return render_template('chat.html')  # Affiche la page HTML du chat

# Fonction qui gère les messages reçus
@socketio.on('message')
def handleMessage(msg):
    print('Message reçu :', msg)  # Affiche le message dans le terminal
    send(msg, broadcast=True)     # Envoie le message à tous les clients connectés

# Démarrage de l'application
if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=10000)

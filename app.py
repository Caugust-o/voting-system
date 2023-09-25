CSS = """
    body {
        font-family: Arial, sans-serif;
        margin: 40px;
        text-align: center;
        background-color: #f4f4f4;
    }

    .container {
        background-color: #fff;
        padding: 20px;
        border-radius: 5px;
        box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
        max-width: 500px;
        margin: 0 auto;
    }

    h1, h2 {
        color: #333;
    }

    button {
        padding: 10px 15px;
        border: none;
        background-color: #007bff;
        color: #fff;
        border-radius: 3px;
        cursor: pointer;
        margin-top: 10px;
    }

    button:hover {
        background-color: #0056b3;
    }
"""

from flask import Flask, render_template, request, redirect, url_for
from collections import Counter

app = Flask(__name__)

users = set()
votes = Counter()

@app.route('/')
def home():
    if not session.get('voting_started'):
        return f"""
        <style>{CSS}</style>
        <div class="container">
            <h1>Registro de Votação</h1>
            <form action="/register" method="post">
                Nome: <input type="text" name="name">
                <button type="submit">Registrar</button>
            </form>
        </div>
        """
    else:
        return f"""
        <style>{CSS}</style>
        <div class="container">
            <h1>Votação em andamento</h1>
            <h2>Escolha uma opção:</h2>
            <form action="/vote" method="post">
                <button name="choice" value="Option1">Opção 1</button>
                <button name="choice" value="Option2">Opção 2</button>
            </form>
        </div>
        """
@app.route('/add_user', methods=['POST'])
def add_user():
    username = request.form['username']
    if username not in users:
        users.add(username)
        return redirect(url_for('vote'))
    return "Usuário já registrado!"

@app.route('/vote')
def vote():
    return render_template('vote.html')

@app.route('/submit_vote', methods=['POST'])
def submit_vote():
    choice = request.form['choice']
    username = request.form['username']
    if username in users and username not in votes:
        votes[username] = choice
        return "Voto registrado!"
    return "Erro ao registrar voto!"

@app.route('/results')
def results():
    if not session.get('voting_started'):
        return redirect('/')
    else:
        total_votes = len(session['votes']['Option1']) + len(session['votes']['Option2'])
        option1_percentage = (len(session['votes']['Option1']) / total_votes) * 100
        option2_percentage = (len(session['votes']['Option2']) / total_votes) * 100
        return f"""
        <style>{CSS}</style>
        <div class="container">
            <h1>Resultados</h1>
            <h2>Opção 1: {option1_percentage:.2f}%</h2>
            <h2>Opção 2: {option2_percentage:.2f}%</h2>
        </div>
        """
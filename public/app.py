from flask import Flask, render_template, request, redirect, session, jsonify
import mysql.connector

app = Flask(__name__)
app.secret_key = 'chave-teste'

@app.route('/')
def form():
    return render_template('form.html')

@app.route('/inserir', methods=['POST'])
def inserir():
    dados = request.get_json()
    nome = dados.get('nome', 0)
    email = dados.get('email', 0)
    senha = dados.get('senha', 0)

    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        port=3306,
        password="813813",
        database="mines"
    )

    mycursor = mydb.cursor()
    sql = "INSERT INTO usuario (nome, email, senha) VALUES (%s, %s, %s)"
    valores = (nome, email, senha)
    mycursor.execute(sql, valores)
    mydb.commit()

    return redirect('/login')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/minigame')
def minigame():
    return render_template('minigame.html')

@app.route('/logar', methods=['POST'])
def logar():
    dados = request.get_json()
    email = dados.get('email', 0)
    senha = dados.get('senha', 0)

    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        port=3306,
        password="813813",
        database="mines"
    )

    mycursor = mydb.cursor(dictionary=True)
    sql = "SELECT * FROM usuario WHERE email = %s AND senha = %s"
    mycursor.execute(sql, (email, senha))
    usuario = mycursor.fetchone()

    if usuario:
        session['usuario'] = usuario['nome']
        return redirect('/minigame')
    else:
        return jsonify({'sucesso': False})

@app.route('/pontuacao')
def pontuacao():
    return render_template('pontuacao.html')

@app.route('/inserir_pontuacao', methods=['POST'])
def inserir_pontuacao():
    dados = request.get_json()
    acertos = dados.get('acertos', 0)
    erros = dados.get('erros', 0)

    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        port=3306,
        password="813813",
        database="mines"
    )

    mycursor = mydb.cursor()
    sql = "INSERT INTO pontuacao (acertos) VALUES (%s)"
    try:
        mycursor.execute(sql, (acertos, erros))
        mydb.commit()
        return jsonify({'sucesso': True})
    except Exception as e:
        print("Erro ao inserir pontuação:", e)
        return jsonify({'sucesso': False})

app.run(debug=True)
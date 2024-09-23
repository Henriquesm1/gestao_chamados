from flask import Blueprint, render_template, redirect, url_for, flash, request
from ..models import db, User
from werkzeug.security import generate_password_hash

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        nivel = request.form['nivel']

        if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
            flash('Nome de usuário ou email já estão em uso. Por favor, escolha outro.', 'danger')
            return redirect(url_for('auth.register'))
        
        novo_usuario = User(username=username, email=email, password=password, nivel=nivel)
        db.session.add(novo_usuario)
        db.session.commit()

        flash('Usuário registrado com sucesso!', 'success')
        return redirect(url_for('auth.login'))

    return render_template('register_user.html')

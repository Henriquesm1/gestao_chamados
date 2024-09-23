from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required,current_user
from ..models import db, User  
from werkzeug.security import generate_password_hash

usuarios_bp = Blueprint('usuarios', __name__, url_prefix='/usuarios')

@usuarios_bp.route('/')
def listar_usuarios():
    usuarios = User.query.all()
    print(f"[INFO] Total de usuários listados: {len(usuarios)}")  # Log para verificar a quantidade de usuários
    return render_template('listar_usuarios.html', usuarios=usuarios)


@usuarios_bp.route('/criar', methods=['GET', 'POST'])
def criar_usuario():
    if request.method == 'POST':
        username = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        perfil = request.form['perfil']

        print(f"[INFO] Tentando criar usuário: {username}, {email}, {perfil}")

        if User.query.filter_by(email=email).first():
            print("[WARNING] E-mail já cadastrado!")
            flash('E-mail já cadastrado!', 'danger')
            return redirect(url_for('usuarios.criar_usuario'))
        
        senha_hash = generate_password_hash(senha, method='pbkdf2:sha256')

        novo_usuario = User(username=username, email=email, perfil=perfil, password_hash=senha_hash)
        db.session.add(novo_usuario)
        db.session.commit()
        print(f"[INFO] Usuário criado com sucesso: {username}")
        flash('Usuário criado com sucesso!', 'success')
        return redirect(url_for('usuarios.listar_usuarios'))

    return render_template('criar_usuario.html')
    
@usuarios_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_usuario(id):
    usuario = User.query.get_or_404(id)
    print(f"[INFO] Editando usuário: {usuario.username}")  

    if request.method == 'POST':
        usuario.username = request.form['nome']
        usuario.email = request.form['email']
        usuario.perfil = request.form['perfil']
        if request.form['senha']:
            usuario.password = request.form['senha']
            print("[INFO] Senha do usuário foi atualizada.") 

        db.session.commit()
        print("[INFO] Usuário atualizado com sucesso.")  
        flash('Usuário atualizado com sucesso!', 'success')
        return redirect(url_for('usuarios.listar_usuarios'))

    return render_template('editar_usuario.html', usuario=usuario)

@usuarios_bp.route('/deletar/<int:id>', methods=['POST'])
def deletar_usuario(id):
    usuario = User.query.get_or_404(id)
    db.session.delete(usuario)
    db.session.commit()
    print(f"[INFO] Usuário deletado com sucesso: {usuario.username}")  
    flash('Usuário deletado com sucesso!', 'success')
    return redirect(url_for('usuarios.listar_usuarios'))

@usuarios_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        print(f"[INFO] Tentativa de login com e-mail: {email}")  

        usuario = User.query.filter_by(email=email).first()

        if usuario:
            print(f"[INFO] Usuário encontrado: {usuario.username}")  
            if usuario.check_password(senha):
                print("[INFO] Senha correta.")  
                login_user(usuario)
                flash('Login realizado com sucesso!', 'success')

                if usuario.perfil == 'admin':
                    return redirect(url_for('dashboard.dashboard'))
                elif usuario.perfil == 'analista':
                    return redirect(url_for('chamados.listar_chamados'))
                elif usuario.perfil == 'tecnico':
                    return redirect(url_for('chamados.listar_chamados'))
                else:
                    return redirect(url_for('chamados.listar_chamados'))  
            else:
                print("[WARNING] Senha incorreta.")  
        else:
            print("[WARNING] Usuário não encontrado.")  

        flash('E-mail ou senha incorretos.', 'danger')

    return render_template('login.html')

@usuarios_bp.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    print("[INFO] Usuário desconectado.")  
    flash('Você foi desconectado.', 'success')
    return redirect(url_for('usuarios.login'))




@usuarios_bp.route('/alterar_senha/<int:id>', methods=['GET', 'POST'])
def alterar_senha(id):
    if current_user.id != id and current_user.perfil != 'admin':
        return {'message': 'Você não tem permissão para alterar esta senha.', 'status': 'error'}, 403

    usuario = User.query.get_or_404(id)

    if request.method == 'POST':
        nova_senha = request.form['senha']
        nova_senha_hash = generate_password_hash(nova_senha, method='pbkdf2:sha256')
        usuario.password_hash = nova_senha_hash
        db.session.commit()
        
        return {'message': 'Senha alterada com sucesso!', 'status': 'success', 'redirect_url': url_for('dashboard.dashboard')}, 200

    return render_template('base.html', usuario=usuario)



from app import create_app
from app.models import db, User
from werkzeug.security import generate_password_hash

# Inicializa a aplicação
app = create_app()

# Dados do novo usuário admin
username = ''
email = ''
password = ''  # Altere para uma senha forte de sua escolha
perfil = ''

# Função para criar o usuário admin
def create_admin_user():
    with app.app_context():
        # Verifica se o usuário já existe
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            print("Usuário admin já existe.")
            return

        # Cria o hash da senha usando um método consistente
        password_hash = generate_password_hash(password, method='pbkdf2:sha256')
        
        # Cria o novo usuário admin
        new_admin = User(
            username=username,
            email=email,
            password_hash=password_hash,
            perfil=perfil
        )
        
        # Adiciona e confirma no banco de dados
        db.session.add(new_admin)
        db.session.commit()
        print("Usuário admin criado com sucesso.")

# Executa a função para criar o usuário admin
if __name__ == "__main__":
    create_admin_user()

import logging
from flask import Blueprint, render_template, request, redirect, url_for, flash
from ..models import db, Categoria

# Configuração do logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

categorias_bp = Blueprint('categorias', __name__, url_prefix='/categorias')

@categorias_bp.route('/')
def listar_categorias():
    logger.info("Rota '/' acessada com método GET para listar categorias.")
    categorias = Categoria.query.all()
    logger.info(f"Listando categorias, total encontrado: {len(categorias)}")
    return render_template('listar_categorias.html', categorias=categorias)

@categorias_bp.route('/nova', methods=['GET', 'POST'])
def nova_categoria():
    logger.info(f"Rota '/nova' acessada com método: {request.method}")

    if request.method == 'POST':
        logger.info("Recebendo dados do formulário para criar nova categoria.")
        
        nome = request.form.get('nome')
        descricao = request.form.get('descricao')
        logger.info(f"Dados recebidos - Nome: {nome}, Descrição: {descricao}")

        if not nome:
            logger.warning("O campo nome está vazio, não pode prosseguir.")
            flash('Nome da categoria é obrigatório.', 'danger')
            return redirect(url_for('categorias.nova_categoria'))

        nova_categoria = Categoria(nome=nome, descricao=descricao)
        db.session.add(nova_categoria)
        try:
            db.session.commit()
            logger.info(f"Categoria '{nome}' criada com sucesso.")
            flash('Categoria criada com sucesso!', 'success')
        except Exception as e:
            db.session.rollback()
            logger.error(f"Erro ao criar categoria: {e}")
            flash('Erro ao criar categoria. Por favor, tente novamente.', 'danger')

        return redirect(url_for('categorias.listar_categorias'))
    
    logger.info("Renderizando formulário para nova categoria.")
    return render_template('nova_categoria.html')

import hashlib
import traceback

from flask import redirect
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from flask_openapi3 import OpenAPI, Info, Tag
from flask_restful import Api, reqparse

from model.usuario import UserModel
from schemas.error import ErrorAuthorizationSchema, ErrorSchema, ServerErrorSchema
from schemas.usuario import ListagemUsuariosApiSchema, RemoveSchema, UserBody
from schemas.usuario import UserBodyRet, UserPath, RegisterSchema, UserVerify, VerificaSchema

import os
from dotenv import load_dotenv

load_dotenv()

info = Info(title="API Usuário", version="1.0.0", description="API para gerenciar usuários\n\n Para obter o token use a api de TOKEN.")
app = OpenAPI(__name__, info=info)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')

api = Api(app)
jwt = JWTManager(app)

CORS(app, resources={r"/api/*": {"origins": "http://127.0.0.1:5000"}})

@app.before_request
def cria_banco():
    banco.create_all()

home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger")
usuario_tag = Tag(name="Usuário", description="Rotas para Usuário")

security_scheme = {
    "Bearer Token": {
        "type": "http",
        "scheme": "bearer",
        "bearerFormat": "JWT"
    }
}
app.security_schemes = security_scheme

@app.get('/', tags=[home_tag], doc_ui=False)
def home():
    """ Home da aplicação.

        Redireciona para /openapi/swagger, abrindo a documentação da API.
    """
    return redirect('/openapi/swagger')

@app.get('/api/usuarios', 
         tags=[usuario_tag], 
         responses={
                    "200": ListagemUsuariosApiSchema, 
                    "400": ErrorSchema, 
                    "401": ErrorAuthorizationSchema, 
                    "500": ServerErrorSchema}, 
         security=[{"Bearer Token": []}])
@jwt_required()
def users():
    """ Lista de usuários.

        Traz todos os usuários se tiver a chave de acesso.
    """
    try:
        users = [users.json() for users in UserModel.query.all()]
        return {'Users': users}, 200
    except:
        return {'error': 'Server error'}, 500

@app.post('/api/registrar', tags=[usuario_tag],
           responses={
                    "201": RegisterSchema, 
                    "400": ErrorSchema, 
                    "500": ServerErrorSchema})

def usuario_novo(body:RegisterSchema):
    """ Cria um novo usuário.

        Cria um usuário caso tenha a chave de acesso.
    """
    atributos = reqparse.RequestParser()
    atributos.add_argument('login', type=str, required=True)
    atributos.add_argument('senha', type=str, required=True)
    atributos.add_argument('nivel', type=int, required=True)
    atributos.add_argument('email', type=str, required=True)
    atributos.add_argument('ativado', type=str)
    dados = atributos.parse_args()

    if not dados['email'] or dados['email'] is None:
        return {"message": "O campo 'email' precisa estar preenchido."}, 400
    
    if UserModel.find_by_email(dados['email']):
        return {"message": "O email'{}' já existe.".format(dados['email'])}, 400

    if UserModel.find_by_login(dados['login']):
        return {"message": "O login'{}' já existe.".format(dados['login'])}, 400

    senha_hash = hashlib.sha256(dados['senha'].encode()).hexdigest()
    dados['senha'] = senha_hash
    
    user = UserModel(**dados)
    user.ativado = 'S' 
    try:
        user.save_user()
    except:
        user.delete_user()
        traceback.print_exc()
        return {"message": "Um erro aconteceu."}, 500 
    
    token_de_acesso = create_access_token(identity=user.user_id)
    return {
            'message': 'Usuário criado com sucesso!',
            'access_token': token_de_acesso,
            'login':dados['login'],
            'nivel':dados['nivel']
            }, 201

@app.put('/api/usuario/<int:id>', tags=[usuario_tag], 
         responses={
                    "200": UserBodyRet, 
                    "400": ErrorSchema, 
                    "401": ErrorAuthorizationSchema, 
                    "500": ServerErrorSchema},
         security=[{"Bearer Token": []}])
@jwt_required()
def update_user(path: UserPath, body: UserBody):
    """Atualizar um usuário
    
        Atualiza o nome, email, senha e nível de um usuário existente.
    """
    user = UserModel.find_user(path.id)

    if user:
        try:
            user.email = body.email if body.email else user.email
            user.senha = hashlib.sha256(body.senha.encode()).hexdigest() if body.senha else user.senha
            user.nivel = body.nivel if body.nivel else user.nivel
            user.ativado = body.ativado.upper() if body.ativado else user.ativado

            user.save_user()

            return user.json(), 200
        except Exception as e:
            banco.session.rollback()  
            return {'message': f'Erro ao atualizar o usuário: {str(e)}'}, 500
    return {'message': 'Usuário não encontrado'}, 404

@app.delete('/api/usuario/<int:id>', tags=[usuario_tag], 
            responses={
                    "204": RemoveSchema, 
                    "400": ErrorSchema, 
                    "404": ErrorSchema, 
                    "401": ErrorAuthorizationSchema, 
                    "500": ServerErrorSchema}, 
            security=[{"Bearer Token": []}])
@jwt_required()
def delete_User(path: UserPath):
    """Deleta um usuário
    
        Deleta um usuário existente.
    """
    success = UserModel.delete_by_id(path.id)  
    if success:
        return {"message": "Usuário deletado com sucesso"}, 204
    return {"message": "Usuário não encontrado"}, 404

@app.post('/api/verifica_senha', tags=[usuario_tag],
          responses={
                    "201": VerificaSchema, 
                    "400": ErrorSchema, 
                    "404": ErrorSchema, 
                    "500": ServerErrorSchema} )
def verifica_senha(body: UserVerify):
    """Verifica conexão
    
        Verifica se existe o usuário e valida os dados passados.
    """
    
    user = UserModel.find_by_login(body.login)
    
    if user:
        if user.senha == body.senha:
            if user.ativado:
                return {'user_id': user.user_id,
                        'nivel': user.nivel,
                        'login': body.login,
                        'ativado': user.ativado 
                        }, 201
            return {'message': 'Usuário não confirmado.'}, 400
    return {'message': 'Credenciais inválidas. Verifique o login e a senha.'}, 400
    
if __name__ == '__main__':
    from sql_alchemy import banco
    banco.init_app(app)
    app.run(debug=True, host='0.0.0.0', port=5001)
# TR4CKER-API :page_with_curl:

API desenvolvida em Python para tracking das músicas mais ouvidas no Brasil de determinado artista no Spotify.
O front-end da aplicação está disponível em https://tr4cker.netlify.app/

## Feats :star2:	

- Login e registro de usuário, com autenticação nas funcionalidades.
- Integração com a API oficial do Spotify para as consultas informadas.
- É possível salvar os artistas preferidos para facilitar novas consultas.

## Ferramentas utilizadas :hammer_and_wrench:

- Django
- PostgreSQL
- PyJWT
- PyTest
- Faker (para os testes com PyTest)

## Endpoints :mag_right:

#### - /register
#### - /login
#### - /user/:id :closed_lock_with_key: 
#### - /users :closed_lock_with_key:
#### - /artist/:id :closed_lock_with_key:
#### - /artist :closed_lock_with_key:
#### - /artist-list/:id :closed_lock_with_key:

## Como rodar o projeto

- Clone o repositório
- Instale as dependências
- Crie um banco de dados Postgres e o configure em ```settings.py```
- É necessário configurar, na raíz do projeto, um .env com um ```CLIENT_ID``` e um ```CLIENT_SECRET``` para a interação com a API do Spotify. Mais informações em https://developer.spotify.com/documentation/web-api
- ```python3 manage.py runserver``` para rodar o projeto
#### Para executar os testes 

- Crie ao menos quatro usuários no banco de dados. Logo após, adicione ```admin_user``` e ```admin_email``` no arquivo .env com as credenciais de um usuário
cadastrado no banco. Por fim, execute ```pytest``` para rodar os testes.

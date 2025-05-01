
Este é um sistema  feito em Python para gerenciar cursos.

 Funcionalidades

- Cadastro de alunos com nome, email e curso
- Cursos com valores diferentes
- Simulação de pagamento (fictício)
- Listagem de todos os inscritos
- Busca por nome, email ou curso
- Edição e exclusão de alunos
- Exportação da lista para Excel e PDF



 Como usar

1. Crie o banco de dados MySQL:

```sql
CREATE DATABASE inscricoes_db;

2. No código, altere password com a senha do seu MySQL.

3. Instale as dependências:

pip install pymysql pandas openpyxl fpdf2

4. Rode o sistema:

python sistema_inscricoes.py

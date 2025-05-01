import pymysql
import pandas as pd
from fpdf import FPDF

db = pymysql.connect(
    host="localhost",
    user="root",
    password="sua_senha",
    database="inscricoes_db"
)

cursor = db.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS inscritos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100),
    email VARCHAR(100),
    curso VARCHAR(100),
    valor DECIMAL(10,2)
)
""")
db.commit()

cursos = {
    "Python Básico": 200.00,
    "Flask Avançado": 350.00,
    "Data Science": 500.00
}

def cadastrar_aluno():
    nome = input("Nome: ")
    email = input("Email: ")
    for i, (curso, valor) in enumerate(cursos.items(), start=1):
        print(f"{i}. {curso} - R$ {valor:.2f}")
    escolha = int(input("Escolha o número do curso: "))
    curso = list(cursos.keys())[escolha - 1]
    valor = cursos[curso]
    input("Pressione Enter para simular o pagamento...")
    cursor.execute("INSERT INTO inscritos (nome, email, curso, valor) VALUES (%s, %s, %s, %s)",
                   (nome, email, curso, valor))
    db.commit()
    print("Aluno cadastrado com sucesso!")

def listar_inscritos():
    cursor.execute("SELECT * FROM inscritos")
    for row in cursor.fetchall():
        print(row)

def buscar_inscrito():
    termo = input("Digite nome, email ou curso: ")
    cursor.execute("""
        SELECT * FROM inscritos
        WHERE nome LIKE %s OR email LIKE %s OR curso LIKE %s
    """, (f"%{termo}%", f"%{termo}%", f"%{termo}%"))
    for row in cursor.fetchall():
        print(row)

def editar_inscrito():
    listar_inscritos()
    aluno_id = input("Digite o ID do aluno para editar: ")
    novo_nome = input("Novo nome: ")
    novo_email = input("Novo email: ")
    for i, (curso, valor) in enumerate(cursos.items(), start=1):
        print(f"{i}. {curso} - R$ {valor:.2f}")
    escolha = int(input("Escolha o número do novo curso: "))
    novo_curso = list(cursos.keys())[escolha - 1]
    novo_valor = cursos[novo_curso]
    cursor.execute("""
        UPDATE inscritos SET nome=%s, email=%s, curso=%s, valor=%s WHERE id=%s
    """, (novo_nome, novo_email, novo_curso, novo_valor, aluno_id))
    db.commit()
    print("Aluno atualizado.")

def excluir_inscrito():
    listar_inscritos()
    aluno_id = input("Digite o ID do aluno para excluir: ")
    cursor.execute("DELETE FROM inscritos WHERE id=%s", (aluno_id,))
    db.commit()
    print("Aluno excluído.")

def exportar_excel():
    cursor.execute("SELECT * FROM inscritos")
    rows = cursor.fetchall()
    df = pd.DataFrame(rows, columns=["ID", "Nome", "Email", "Curso", "Valor"])
    df.to_excel("inscritos.xlsx", index=False)
    print("Exportado para inscritos.xlsx")

def exportar_pdf():
    cursor.execute("SELECT * FROM inscritos")
    rows = cursor.fetchall()
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Lista de Inscritos", ln=True, align="C")
    pdf.ln()
    for row in rows:
        linha = f"ID: {row[0]} | Nome: {row[1]} | Email: {row[2]} | Curso: {row[3]} | R$ {row[4]}"
        pdf.cell(200, 10, txt=linha, ln=True)
    pdf.output("inscritos.pdf")
    print("Exportado para inscritos.pdf")

def menu():
    while True:
        print("\n1. Cadastrar")
        print("2. Listar")
        print("3. Buscar")
        print("4. Editar")
        print("5. Excluir")
        print("6. Exportar Excel")
        print("7. Exportar PDF")
        print("0. Sair")
        opcao = input("Opção: ")
        if opcao == "1":
            cadastrar_aluno()
        elif opcao == "2":
            listar_inscritos()
        elif opcao == "3":
            buscar_inscrito()
        elif opcao == "4":
            editar_inscrito()
        elif opcao == "5":
            excluir_inscrito()
        elif opcao == "6":
            exportar_excel()
        elif opcao == "7":
            exportar_pdf()
        elif opcao == "0":
            break

if __name__ == "__main__":
    menu()
    cursor.close()
    db.close()

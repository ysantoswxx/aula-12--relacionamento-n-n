# Relacionamentos Muitos para muitos (N:N)

# Estudantes se inscrevem em cursos.
# um estudante pode fazer vários cursos
# um curso pode ter vários estudantes

# Forma simples:
# A relação não precisa guardar dados extras
# Só fazer o relacionamento

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

Base = declarative_base()

#Tabela Intermediária
inscricoes = Table(
    "inscricoes", #nome da tabela
    Base.metadata,
    Column("aluno_id", Integer, ForeignKey("alunos.id"), primary_key=True),
    Column("curso_id", Integer, ForeignKey("cursos.id"), primary_key=True),
)

# Tabelas curso e aluno
class Aluno(Base):
    __tablename__ = "alunos"

    #Como cria uma coluna
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)

    #Relacionamento
    cursos = relationship("Curso", secondary=inscricoes, back_populates="alunos")

    #Função para imprimir
    def __repr__(self):
        return f"ID: {self.id} - NOME: {self.nome}"

class Curso(Base):
    __tablename__ = "cursos"

    #Como cria uma coluna
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)

    alunos = relationship("Aluno", secondary=inscricoes, back_populates="cursos")

    #Função para imprimir
    def __repr__(self):
        return f"ID: {self.id} - NOME: {self.nome}"
   

#Conexão com db
engine = create_engine("sqlite:///gestao_escolar.db")

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)


#Criar
def cadastrar_curso():
    with Session() as session:
        try:
            #Criar o objeto curso
            nome_curso = input("Digite o nome do curso: ").capitalize()
            curso = Curso(nome=nome_curso)
            #Adicionar no banco
            session.add(curso)  
            #Salvar
            session.commit()        
            print(f"Curso {nome_curso} cadastrado com sucesso!")
        except Exception as erro:
            session.rollback()
            print(f"Ocorreu um erro {erro}")

# cadastrar_curso()

def cadastrar_aluno():
    with Session() as session:
        try:
            #Buscar o curso do aluno
            nome_curso = input("Digite o nome do curso para cadastrar o aluno: ").capitalize()
            curso = session.query(Curso).filter_by(nome=nome_curso).first()
            if curso == None:
                print(f"Nenhum curso encontrado com esse nome {nome_curso}")
                return
            else:
                nome_aluno = input("Digite o nome do aluno para cadastrar: ").capitalize()
                aluno = Aluno(nome=nome_aluno)
                aluno.cursos.append(curso)

                session.add(aluno)
                session.commit()
                print(f"Aluno cadastrado com sucesso!")
        except Exception as erro:
            session.rollback()
            print(f"Ocorreu um erro {erro}")


# cadastrar_aluno()

def adicionar_curso():
    with Session() as session:
        try:
            #Buscar o curso do aluno
            nome_curso = input("Digite o nome do curso para inserir o aluno: ").capitalize()
            curso = session.query(Curso).filter_by(nome=nome_curso).first()
            if curso == None:
                print(f"Nenhum curso encontrado com esse nome {nome_curso}")
                return
            else:
                nome_aluno = input("Digite o nome do aluno para cadastrar: ").capitalize()
                aluno = session.query(Aluno).filter_by(nome=nome_aluno).first()
                if aluno == None:
                    print(f"Nenhum aluno cadastro com esse nome {nome_aluno}")
                    return
                else:
                    aluno.cursos.append(curso)
                    session.commit()
                    print(f"Aluno registro com sucesso no curso {nome_curso}")
        except Exception as erro:
            session.rollback()
            print(f"Ocorreu um erro {erro}")
# adicionar_curso()

#Listar
def listar_cursos():
    with Session() as session:
        try:
            #Como pegar todos os registros da tabela?
            todos_cursos = session.query(Curso).all()
            for curso in todos_cursos:
                print(f"\n--- Curso {curso.nome} ---")
                for aluno in curso.alunos:
                    print(aluno.nome)
        except Exception as erro:
            session.rollback()
            print(f"Ocorreu um erro {erro}")
# listar_cursos()

def listar_alunos():
    with Session() as session:
        try:
            #Como pegar todos os registros da tabela?
            todos_alunos = session.query(Aluno).all()
            for aluno in todos_alunos:
                nomes_cursos = [curso.nome for curso in aluno.cursos]
                print(f"Nome: {aluno.nome} - Cursos: {nomes_cursos}")
        except Exception as erro:
            session.rollback()
            print(f"Ocorreu um erro {erro}")

listar_alunos()
#Atualizar

def atualizar_aluno():
    with Session() as session:
        try:
            nome_antigo = input("Digite o nome do aluno que deseja atualizar: ").capitalize()
            aluno = session.query(Aluno).filter_by(nome=nome_antigo).first()

            if aluno == None:
                print("Aluno não encontrado!")
                return

            novo_nome = input("Digite o novo nome: ").capitalize()
            aluno.nome = novo_nome

            session.commit()
            print("Aluno atualizado com sucesso!")

        except Exception as erro:
            session.rollback()
            print(f"Ocorreu um erro {erro}")

def atualizar_curso_do_aluno():
    with Session() as session:
        try:
            nome_aluno = input("Digite o nome do aluno: ").capitalize()
            aluno = session.query(Aluno).filter_by(nome=nome_aluno).first()

            if aluno == None:
                print("Aluno não encontrado!")
                return

            nome_curso_antigo = input("Digite o curso que deseja remover: ").capitalize()
            curso_antigo = session.query(Curso).filter_by(nome=nome_curso_antigo).first()

            nome_curso_novo = input("Digite o novo curso: ").capitalize()
            curso_novo = session.query(Curso).filter_by(nome=nome_curso_novo).first()

            if curso_antigo in aluno.cursos:
                aluno.cursos.remove(curso_antigo)

            aluno.cursos.append(curso_novo)

            session.commit()
            print("Curso atualizado com sucesso!")

        except Exception as erro:
            session.rollback()
            print(f"Ocorreu um erro {erro}")

#Deletar

def deletar_aluno():
    with Session() as session:
        try:
            nome_aluno = input("Digite o nome do aluno para deletar: ").capitalize()
            aluno = session.query(Aluno).filter_by(nome=nome_aluno).first()

            if aluno == None:
                print("Aluno não encontrado!")
                return

            session.delete(aluno)
            session.commit()

            print("Aluno deletado com sucesso!")

        except Exception as erro:
            session.rollback()
            print(f"Ocorreu um erro {erro}")


def remover_aluno_do_curso():
    with Session() as session:
        try:
            nome_aluno = input("Digite o nome do aluno: ").capitalize()
            aluno = session.query(Aluno).filter_by(nome=nome_aluno).first()

            nome_curso = input("Digite o curso para remover: ").capitalize()
            curso = session.query(Curso).filter_by(nome=nome_curso).first()

            if aluno == None or curso == None:
                print("Aluno ou curso não encontrado!")
                return

            if curso in aluno.cursos:
                aluno.cursos.remove(curso)
                session.commit()
                print("Aluno removido do curso com sucesso!")
            else:
                print("Esse aluno não está nesse curso!")

        except Exception as erro:
            session.rollback()
            print(f"Ocorreu um erro {erro}")
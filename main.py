#Relacionamento Muitos para muitos (N:N)

#Estudantes se inscreve em cursos.
# um estudante pode fazer vários cursos

# Forma simples:
# A relação não precisa guardar dados extras
# Só fazer o relacionamento

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

Base = declarative_base()

# Tableas curso e aluno
class Aluno(Base):
    __tablename__ = "alunos"

    #Como cria uma coluna
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)

    #Função para imprimir
    def __repr__(self):
        return f"ID: {self.id} - NOME: {self.nome}"

class Curso(Base):
    __tablename__ = "cursos"

    #Como cria uma coluna
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)

    #Função para imprimir
    def __repr__(self):
        return f"ID: {self.id} - NOME: {self.nome}"


#Tabela Intermediária
inscricoes = Table(
    "inscricoes", #nome da tabela
    Base.metadata,
    Column("aluno_id", Integer, ForeignKey("alunos.id")),
    Column("curso_id", Integer, ForeignKey("cursos.id")),
)   

#Conexão com db
engine = create_engine("sqlite:///gestao_escolar.db")

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)

#criar 
def cadastrar_curso():
    with Session() as session:
        try:
            nome_curso = input("Digite o nome do curso: ").capitalize()
            curso = Curso(nome=nome_curso)

            session.add(curso)
            #salvar
            session.commit()
            print(f"Curso {nome_curso} cadastrado com sucesso!!")

        except Exception as erro:
            session.rollback()
            print(f"Ocorreu um erro {erro}")

#listar

#atualizar

#

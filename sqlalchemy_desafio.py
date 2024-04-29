
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DECIMAL
from sqlalchemy.orm import sessionmaker, relationship, declarative_base

import json

# Criando uma conexão com o banco de dados SQLite
engine = create_engine("sqlite://")

# Criando uma classe base para definição das tabelas
Base = declarative_base()

class Cliente(Base):
    __tablename__ = "cliente"
    id = Column(Integer, primary_key=True)
    nome = Column(String(50))
    cpf = Column(String(9))
    endereco = Column(String(50))
    contas = relationship("Conta", back_populates="cliente")

class Conta(Base):
    __tablename__ = "conta"
    id = Column(Integer, primary_key=True)
    tipo = Column(String(10))
    agencia = Column(String(10))
    num = Column(Integer)
    id_cliente = Column(Integer, ForeignKey("cliente.id"))
    saldo = Column(DECIMAL(precision=2))

    # Criando um relacionamento entre Cliente e Conta
    cliente = relationship("Cliente", back_populates="contas")

# Criando as tabelas no banco de dados
Base.metadata.create_all(engine)



if __name__ == "__main__":
    Session = sessionmaker(bind=engine)
    session = Session()

    # Criando um cliente
    novo_cliente = Cliente(nome="Wellington", cpf="123456789", endereco="Rua A, 1")
    session.add(novo_cliente)

    # Criando uma conta associada ao cliente
    nova_conta = Conta(tipo="Corrente", agencia="001", num=12345, id_cliente=novo_cliente.id, saldo=1000.0)
    session.add(nova_conta)

    session.commit()
    

    # Consultando Cliente com ID 1 e suas contas
    cliente_id = 1
    cliente_especifico = session.query(Cliente).filter_by(id=cliente_id).first()

    if cliente_especifico:
        print(f"Cliente: {cliente_especifico.nome}")
        for conta in cliente_especifico.contas:
            print(f"  Conta {conta.id}: Tipo {conta.tipo}, Saldo {conta.saldo}")
    else:
        print(f"Cliente com ID {cliente_id} não encontrado.")



    



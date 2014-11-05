from sqlalchemy import (
    Table,
    Column,
    Index,
    Integer,
    Unicode,
    String,
    DateTime,
    ForeignKey,
    Numeric,
    )

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    relationship,
    )


DBSession = scoped_session(sessionmaker())
Base = declarative_base()


racun_imetnik = Table(
    'racun_imetnik', Base.metadata,
    Column('racun_rn', String, ForeignKey('racuni.rn')),
    Column('imetnik_davcna', String, ForeignKey('imetniki.davcna'))
)

imetnik_naslov = Table(
    'imetnik_naslov', Base.metadata,
    Column('imetnik_davcna', String, ForeignKey('imetniki.davcna')),
    Column('naslov_id', Integer, ForeignKey('naslovi.id'))
)


class Racun(Base):
    __tablename__ = 'racuni'
    sSpre = Column(String(1))
    vir = Column(String(1))
    dSpre = Column(DateTime)
    maticnaPps = Column(String(10))
    rn = Column(String(15), primary_key=True, unique=True)
    iban = Column(String(4))

    PopolnoImeRacuna = Column(Unicode(250))
    KratkoImeRacuna = Column(Unicode(140))
    NazivPp = Column(Unicode(35))

    dOdprt = Column(DateTime)
    dZaprt = Column(DateTime)

    vr = Column(String(1))
    reg = Column(String(1))
    eno = Column(String(1))
    imetniki = relationship(
        "Imetnik",
        secondary=racun_imetnik,
        backref="racuni"
    )


class Imetnik(Base):
    __tablename__ = 'imetniki'
    davcna = Column(String(35), primary_key=True, unique=True)
    matSub = Column(String(10))
    prorup = Column(String(5))
    idTuj = Column(String(30))
    drz = Column(String(3))

    PopolnoIme = Column(Unicode(250))
    KratkoIme = Column(Unicode(140))
    Priimek = Column(Unicode(75))
    Ime = Column(Unicode(75))
    naslovi = relationship(
        "Naslov",
        secondary=imetnik_naslov,
        backref="naslovi"
    )


class Naslov(Base):
    __tablename__ = 'naslovi'
    id = Column(Integer, primary_key=True, unique=True)
    sifTipNaslova = Column(String(10))
    TipNaslova = Column(String(5))
    sifDrzava = Column(String(30))
    Drzava = Column(String(80))
    sifObcina = Column(String(3))
    Obcina = Column(String(40))
    sifUlica = Column(String(4))
    Ulica = Column(String(40))
    stHisna = Column(String(3))
    dodatek = Column(String(3))

    sifHsmid = Column(Numeric(8, 0))
    sifNaselje = Column(Unicode(140))
    Naselje = Column(Unicode(75))
    sifPosta = Column(Unicode(75))
    Posta = Column(Unicode(75))

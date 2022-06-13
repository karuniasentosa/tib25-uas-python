from sqlalchemy import Column, String, Integer
from sqlalchemy import select
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy.engine import Engine

# Declarative base yang akan di-inherit oleh setiap model
Base = declarative_base()


class GedungModel(Base):
    """
    Model class untuk tabel gedung
    """
    __tablename__ = 'gedung'
    id = Column(Integer, primary_key=True)
    nama = Column(String, unique=True, nullable=False)
    base_price = Column('base_price_in_hrs', Integer, nullable=False)

    def __init__(self, id, nama, base_price):
        self.id = id
        self.nama = nama
        self.base_price = base_price


class GedungHelper:
    """
    Class helper untuk tabel gedung
    """

    def __init__(self, engine: Engine):
        self.engine = engine

    def create(self, gedung: GedungModel):
        """
        Membuat model gedung baru dan
        memasukkan ke dalam dataase
        :param gedung: gedung baru
        """
        with Session(self.engine) as session:
            session.add(gedung)
            session.commit()

    def update(self, idGedung, newGedung: GedungModel):
        """
        Mengubah salah satu data gedung berdasarkan id gedung
        :param idGedung: id gedung yang dicari
        :param newGedung: gedung baru yang ingin diganit
        """
        the_gedung: GedungModel = self.read_one(idGedung)
        with Session(self.engine) as session:
            the_gedung.nama = newGedung.nama
            the_gedung.base_price = newGedung.base_price
            session.add(the_gedung)
            session.commit()

    def delete(self, idGedung):
        """
        Menghapus salah satu gedung berdasarkan id
        :param idGedung: id gedung yang dicari
        """
        the_gedung: GedungModel = self.read_one(idGedung)
        with Session(self.engine) as session:
            session.delete(the_gedung)
            session.commit()

    def read(self):
        """
        Query semua isi dari tabel gedung
        :return: gedung yang ada di dalab taebl
        """
        with Session(self.engine) as session:
            return session.query(GedungModel)

    def read_one(self, idGedung):
        """
        Query salah satu dari isi tabel gedung
        berdasarkan id
        :param idGedung: yang ingin dicari
        :return: `GedungModel`
        """
        with Session(self.engine) as session:
            stmt = select(GedungModel).where(GedungModel.id == idGedung)
            return session.scalars(stmt).one()

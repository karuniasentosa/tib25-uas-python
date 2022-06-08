from sqlalchemy import Column, String, Integer
from sqlalchemy import select
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy.engine import Engine

# Declarative base yang akan di-inherit oleh setiap model
Base = declarative_base()


class OrganisasiModel(Base):
    """
    Model class untuk tabel organisasi
    """
    __tablename__='organisasi'
    id = Column(Integer, primary_key=True)
    nama_organisasi = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False)
    no_telp = Column(String, nullable=False)

    def __init__(self, id, nama_organisasi, email, no_telp):
        self.id = id
        self.nama_organisasi = nama_organisasi
        self.email = email
        self.no_telp = no_telp


class OrganisasiHelper:
    """
    Class helper untuk tabel organisasi
    """
    def __init__(self, engine: Engine):
        self.engine = engine

    def create(self, organisasi: OrganisasiModel):
        """
        Membuat model organisasi baru dan
        memasukkan ke dalam database
        :param organisasi: organisasi baru
        :return:
        """
        with Session(self.engine) as session:
            session.add(organisasi)
            session.commit()

    def update(self, idOrganisasi, newOrganisasi: OrganisasiModel):
        """
        Mengubah salah satu data organisasi berdasarkan idOrganisasi
        :param idOrganisasi: id organisasi yang dicari
        :param newOrganisasi: organisasi baru yang ingin diganti
        """
        the_organisasi: OrganisasiModel = self.read_one(idOrganisasi)
        with Session(self.engine) as session:
            the_organisasi.nama_organisasi = newOrganisasi.nama_organisasi
            the_organisasi.email = newOrganisasi.email
            the_organisasi.no_telp = newOrganisasi.no_telp
            session.add(the_organisasi)
            session.commit()

    def delete(self, idOrganisasi):
        """
        Menghapus salah satu organisasi berdasarkan id
        :param idOrganisasi: id organisasi yang dicari
        """
        the_organisasi: OrganisasiModel = self.read_one(idOrganisasi)
        with Session(self.engine) as session:
            session.delete(the_organisasi)
            session.commit()

    def read(self):
        """
        Query semua isi dari tabel organisasi
        :return: Organisasi yang di dalam tabel
        """
        with Session(self.engine) as session:
            return session.query(OrganisasiModel)

    def read_one(self, idOrganisasi):
        """
        Query salah satu dari isi tabel organisasi
        berdasarkan idOrganisasi
        :param idOrganisasi: yang ingin dicari
        :return: OrganisasiModel yang dicari
        """
        with Session(self.engine) as session:
            stmt = select(OrganisasiModel).where(OrganisasiModel.id == idOrganisasi)
            return session.scalars(stmt).one()

    def read_one_by_name(self, name):
        """
        Query salahs atu isi dari tebal organisais
        berdasarkan nama organisasi
        :param name: nama organisasi yang ingin dicair
        :return:
        """
        with Session(self.engine) as session:
            stmt = select(OrganisasiModel).where(OrganisasiModel.nama_organisasi == name)
            return session.scalars(stmt).one_or_none()
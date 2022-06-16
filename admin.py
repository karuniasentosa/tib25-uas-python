from sqlalchemy import Column, String, Integer
from sqlalchemy import select
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy.engine import Engine

from flask_login import UserMixin


# Declarative base yang akan di-inherit oleh setiap model
Base = declarative_base()


class AdminModel(UserMixin, Base):
    """
    Model class untuk tabel Admin
    """
    __tablename__ = 'admin'
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)

    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password


class AdminHelper:
    """
    Class helper untuk tabel Anggota
    """
    def __init__(self, engine: Engine):
        self.engine = engine

    def create(self, admin: AdminModel):
        """
        Membuat model admin baru dan
        memasukkan ke dalam database
        :param admin: admin baru
        :return:
        """
        with Session(self.engine) as session:
            session.add(admin)
            session.commit()

    def update(self, idAdmin, newAdmin: AdminModel):
        """
        Mengubah salah satu data buku berdasarkan idAdmin
        :param idAdmin: id admin yang dicari
        :param newAdmin: admin baru yang diganti
        :return:
        """
        the_admin: AdminModel = self.read_one_by_user(idAdmin)
        with Session(self.engine) as session:
            the_admin.username = newAdmin.username
            the_admin.password = newAdmin.password
            session.add(the_admin)
            session.commit()

    def delete(self, idAdmin):
        """
        Menghapus salah satu admin beradasrkan id
        :param idAdmin: id admin yang dicari
        :return:
        """
        the_admin: AdminModel = self.read_one_by_user(idAdmin)
        with Session(self.engine) as session:
            session.delete(the_admin)
            session.commit()

    def read(self):
        """
        Query semua isi dari tabel admin
        TODO: Tidak perlu menampilkan kolom password pada halaman
        :return: Admin yang ada di dalam tabel
        """
        with Session(self.engine) as session:
            return session.query(AdminModel)

    def read_one_by_user(self, username):
        """
        Query salah satu dari isi tabel admin
        berdasarkan username
        :param username: Admin yang akan dicari
        :return:
        """
        with Session(self.engine) as session:
            stmt = select(AdminModel).where(AdminModel.username == username)
            return session.scalars(stmt).one_or_none()

    def read_one(self, id):
        """
        Query salah satu dari isi tabel admin
        berdasarkan id
        :param id: Admin yang akan dicari
        :return:
        """
        with Session(self.engine) as session:
            stmt = select(AdminModel).where(AdminModel.id == id)
            return session.scalars(stmt).one()
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy import select
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy.engine import Engine

from organisasi import OrganisasiModel
from gedung import GedungModel

# Declarative base yang akan di-inherit oleh setiap model
Base = declarative_base()


class BookingModel(Base):
    """
    Model class untuk tabel booking
    """
    __tablename__ = 'booking'
    id = Column(Integer, primary_key=True)
    gedung_id = Column(Integer, ForeignKey(GedungModel.id), nullable=False)
    nama_penanggungjawab = Column(String)
    penyewa = Column(Integer, ForeignKey(OrganisasiModel.id), nullable=False)
    start_date = Column(String, nullable=False)
    end_date = Column(String, nullable=False)
    start_time = Column(String, nullable=False)
    end_time = Column(String, nullable=False)

    def __init__(self, id, gedung_id, nama_penanggungjawab, penyewa, start_datetime, end_datetime, start_time,
                 end_time):
        self.id = id
        self.gedung_id = gedung_id
        self.nama_penanggungjawab = nama_penanggungjawab
        self.penyewa = penyewa
        self.start_date = start_datetime
        self.end_date = end_datetime
        self.start_time = start_time
        self.end_time = end_time


class BookingHelper:
    """
    Class helper untuk table booking
    """

    def __init__(self, engine: Engine):
        self.engine = engine

    def create(self, booking: BookingModel):
        """
        Membuat model booking baru dan
        memasukkan ke dalam database
        :param booking: booking baru
        """
        with Session(self.engine) as session:
            session.add(booking)
            session.commit()

    def update(self, idBooking, newBooking: BookingModel):
        """
        Mengubah salah satu data booking berdasarkan id booking
        :param idBooking: id booking yang ingin dicari
        :param newBooking: booking baru yang ingin diganti
        """
        the_booking: BookingModel = self.read_one(idBooking)
        with Session(self.engine) as session:
            the_booking.gedung_id = newBooking.gedung_id
            the_booking.penyewa = newBooking.penyewa  # TODO: Masuk akal gak sih?
            the_booking.nama_penanggungjawab = newBooking.nama_penanggungjawab
            the_booking.start_datetime = newBooking.start_datetime
            the_booking.end_datetime = newBooking.end_datetime
            session.add(the_booking)
            session.commit()

    def delete(self, idBooking):
        """
        Menghapus salah satu booking berdasarkan id
        :param idBooking: id booking yang dicari
        """
        the_booking: OrganisasiModel = self.read_one(idBooking)
        with Session(self.engine) as session:
            session.delete(the_booking)
            session.commit()

    def read(self):
        """
        Query semua isi dari tabel booking
        :return: booking yang di dalam tabel
        """
        with Session(self.engine) as session:
            return session.query(BookingModel)

    def read_one(self, idBooking):
        """
        Query salah satu dari isi tabel organisasi
        berdasarkan idOrganisasi
        :param idBooking: yang ingin dicari
        :return: OrganisasiModel yang dicari
        """
        with Session(self.engine) as session:
            stmt = select(BookingModel).where(BookingModel.id == idBooking)
            return session.scalars(stmt).one()

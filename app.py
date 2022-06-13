import secrets
from datetime import datetime as dt

from flask import Flask, request, redirect, url_for, render_template, abort, jsonify
from sqlalchemy import create_engine
from flask_login import LoginManager

from flask_login import login_required, current_user

from admin import *
from organisasi import *
from authman import *
from booking import *
from gedung import *

app = Flask(__name__)

engine = create_engine("sqlite:///serbaguna.db")

# Generate security key https://stackoverflow.com/a/54433731
app.config['SECRET_KEY'] = secrets.token_urlsafe(32)  # Python >= 3.6

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'admin_login_view'

admin_helper = AdminHelper(engine)
organisasi_helper = OrganisasiHelper(engine)
booking_helper = BookingHelper(engine)
gedung_helper = GedungHelper(engine)


# login view
@app.route('/admin-login')
def admin_login_view():
    pass


@app.route('/admin')
@login_required
def admin_view():
    """
    Halaman admin (dashboard)
    """
    pass


@app.route('/admin/users')
@login_required
def admin_users_view():
    """
    Halaman admin bagian user
    """
    pass


@app.route('/admin/users/create', methods=["POST"])
@login_required
def admin_users_create():
    username = request.form['username']
    password = request.form['password']
    AuthMan.register(engine, username, password)
    pass


@app.route('/admin/booking')
@login_required
def admin_booking_view():
    """
    Halaman admin bagian booking
    """
    pass


@app.route('/admin/booking/create', methods=['POST'])
@login_required
def admin_booking_create():
    id = int(time.time() * 100)
    gedung_id = int(request.form['gedung_id'])
    penanggungjawab = request.form['penanggungjawab']
    penyewa = int(request.form['penyewa'])
    start_datetime = request.form['start_datetime']
    end_datetime = request.form['end_datetime']
    new_booking = BookingModel(id, gedung_id, penanggungjawab, penyewa, start_datetime, end_datetime)
    booking_helper.create(new_booking)

    return redirect(url_for('admin_booking_view'))


@app.route('/admin/booking/edit/<id>', methods=['post'])
def admin_booking_edit(id):
    the_booking: BookingModel = booking_helper.read_one(id)
    the_booking.gedung_id = request.form['gedung_id']
    the_booking.start_datetime = request.form['start_datetime']
    the_booking.end_datetime = request.form['end_datetime']
    booking_helper.update(id, the_booking)

    return redirect(url_for('admin_booking_view'))


@app.route('/admin/organisasi')
@login_required
def admin_organisasi_view():
    """
    Halaman admin bagian organisasi
    """
    pass


@app.route('/admin/gedung')
@login_required
def admin_gedung_view():
    """
    Halaman admin bagian gedung
    """
    pass


@login_manager.user_loader
def load_user(id):
    return admin_helper.read_one(id)


# @login_manager.unauthorized_callback
# def unauthorized():
#     """
#     Halaman yang di-redirect ketika tidak ada user yang login
#     """
#     # TODO: Buat halaman unauthorized?
#     pass


@app.route('/')
def index_view():
    return render_template('index.html')


@app.route('/booking')
def booking_view():
    orgs = organisasi_helper.read()
    gedungs = gedung_helper.read()
    return render_template('form_booking.html', orgs=orgs, gedungs=gedungs)


@app.route('/booking/create', methods=['post'])
def booking_create():
    nama_penanggungjawab = request.form['nama_penanggungjawab']
    nama_organisasi = request.form['nama_organisasi']
    organisasi: OrganisasiModel = organisasi_helper.read_one_by_name(nama_organisasi)
    email = request.form['email']
    nomor_telp = request.form['nomor_telepon']
    if organisasi is None:
        # Create new organization
        new_id = int(time.time())
        organisasi_helper.create(OrganisasiModel(new_id, nama_organisasi, email, nomor_telp))
        organisasi = organisasi_helper.read_one(new_id)
    start_date = request.form['start_date']
    end_date = request.form['end_date']
    start_time = request.form['start_time']
    end_time = request.form['end_time']
    gedung_id = int(request.form['gedung_id'])
    new_booking = BookingModel(int(time.time()), gedung_id, nama_penanggungjawab, organisasi.id, start_date, end_date,
                               start_time, end_time)
    booking_helper.create(new_booking)

    return redirect(url_for('booking_view'))
    pass


@app.route('/about')
def about_view():
    return render_template('about.html')


@app.route('/_/getcompanymp', methods=['post'])
def get_company_mail_and_phone():
    name = request.form['orgname']
    organisasi: OrganisasiModel = organisasi_helper.read_one_by_name(name)
    if organisasi is None:
        abort(404)
    org_email = organisasi.email
    org_phone = organisasi.no_telp
    jsonData = {'email': org_email, 'phone': org_phone}
    return jsonify(jsonData)


@app.route('/_/calbookprice', methods=['post'])
def calculate_booking_price():
    start_date = dt.strptime(request.form['start_date'], '%Y-%m-%d')
    end_date = dt.strptime(request.form['end_date'], '%Y-%m-%d')
    start_time = dt.strptime(request.form['start_time'], '%H:%M')
    end_time = dt.strptime(request.form['end_time'], '%H:%M')
    gedung: GedungModel = gedung_helper.read_one(request.form['gedung_id'])

    diffdays = (end_date - start_date).days + 1
    diffhour = (end_time.hour - start_time.hour)

    price = gedung.base_price * (diffhour * diffdays)

    return str(price)


if __name__ == '__main__':
    app.run(debug=True)

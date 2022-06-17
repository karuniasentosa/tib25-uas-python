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
@app.route('/admin', methods=['GET', 'POST'])
def admin_login_view():
    if request.method == 'GET':
        if current_user.is_authenticated:
            return redirect(url_for('admin_users_view'))
        return render_template('admin/login.html')
    if request.method == 'POST':
        username = request.form['uname']
        password = request.form['psw']
        can_login = AuthMan.login(engine, username, password)
        if can_login:
            return redirect(url_for('admin_users_view'))
        else:
            return abort(401)


@app.route('/admin/admin')
@login_required
def admin_users_view():
    admins = admin_helper.read()
    return render_template('admin/admin_test.html', users=admins)
    pass


@app.route('/admin/admin/create', methods=["POST"])
@login_required
def admin_users_create():
    username = request.form['username']
    password = request.form['password']
    AuthMan.register(engine, username, password)
    return redirect(url_for('admin_users_view'))


@app.route('/admin/admin/update/<id>', methods=['post'])
@login_required
def admin_users_update(id):
    username = request.form['username']
    old_password = request.form['old_password']
    new_password = request.form['new_password']
    the_admin: AdminModel = admin_helper.read_one(id)
    password_matches = check_password_hash(the_admin.password, old_password)
    if not password_matches:
        abort(401)
        return
    new_password_hash = generate_password_hash(new_password)
    new_admin = AdminModel(id, username, new_password_hash)
    admin_helper.update(id, new_admin)
    return redirect(url_for('admin_users_view'))


@app.route('/admin/admin/delete/<id>', methods=['get'])
@login_required
def admin_user_delete(id):
    admin_helper.delete(id)
    return redirect(url_for('admin_users_view'))


@app.route('/admin/booking')
@login_required
def admin_booking_view():
    booking_list = booking_helper.read()
    return render_template('admin/booking_test.html', booking_list=booking_list)


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
@login_required
def admin_booking_edit(id):
    the_booking: BookingModel = booking_helper.read_one(id)
    the_booking.gedung_id = request.form['gedung_id']
    the_booking.start_datetime = request.form['start_datetime']
    the_booking.end_datetime = request.form['end_datetime']
    booking_helper.update(id, the_booking)

    return redirect(url_for('admin_booking_view'))


@app.route('/admin/booking/delete/<id>', methods=['get'])
@login_required
def admin_booking_delete(id):
    booking_helper.delete(id)
    return redirect(url_for('admin_booking_view'))


@app.route('/admin/organisasi')
@login_required
def admin_organisasi_view():
    orgs = organisasi_helper.read()
    return render_template('admin/organisasi.html', orgs=orgs)
    pass


@app.route('/admin/organisasi/create', methods=['post'])
@login_required
def admin_organisasi_create():
    nama_organisasi = request.form['nama_organisasi']
    email = request.form['email']
    no_telp = request.form['NoTelp']
    id = random.getrandbits(16)
    new_organisasi = OrganisasiModel(id, nama_organisasi, email, no_telp)
    organisasi_helper.create(new_organisasi)

    return redirect(url_for('admin_organisasi_view'))


@app.route('/admin/organisasi/update/<id>', methods=['post'])
@login_required
def admin_organisasi_update(id):
    nama_organisasi = request.form['nama_organisasi']
    email = request.form['email']
    no_telp = request.form['NoTlp']
    the_organisasi: OrganisasiModel = organisasi_helper.read_one(id)
    the_organisasi.nama_organisasi = nama_organisasi
    the_organisasi.email = email
    the_organisasi.no_telp = no_telp
    organisasi_helper.update(id, the_organisasi)

    return redirect(url_for('admin_organisasi_view'))


@app.route('/admin/organisasi/delete/<id>', methods=['get'])
@login_required
def admin_organisasi_delete(id):
    organisasi_helper.delete(id)

    return redirect(url_for('admin_organisasi_view'))


@app.route('/admin/gedung')
@login_required
def admin_gedung_view():
    gedungs = gedung_helper.read()
    return render_template('admin/gedung.html', gedungs=gedungs)


@app.route('/admin/gedung/create', methods=['post'])
@login_required
def admin_gedung_create():
    nama = request.form['nama']
    base_price = request.form['base_price']
    id = random.getrandbits(8)
    new_gedung = GedungModel(id, nama, int(base_price))
    gedung_helper.create(new_gedung)

    return redirect(url_for('admin_gedung_view'))


@app.route('/admin/gedung/update/<id>', methods=['post'])
@login_required
def admin_gedung_update(id):
    nama = request.form['nama_gedung']
    base_price = request.form['baseprice_gedung']
    the_gedung: GedungModel = gedung_helper.read_one(id)
    the_gedung.nama = nama
    the_gedung.base_price = base_price
    gedung_helper.update(id, the_gedung)

    return redirect(url_for('admin_gedung_view'))


@app.route('/admin/gedung/delete/<id>', methods=['get'])
@login_required
def admin_gedung_delete(id):
    gedung_helper.delete(id)
    redirect(url_for('admin_gedung_view'))

    return redirect(url_for('admin_gedung_view'))


@app.route('/admin/logout')
@login_required
def admin_logout():
    AuthMan.logout()
    return redirect(url_for('index_view'))


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
    return render_template('user/form_booking.html', orgs=orgs, gedungs=gedungs)


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
    return render_template('user/about.html')


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


@app.route('/_/templates/admin_edit', methods=['post'])
def templates_admin_edit():
    id = request.form['id']
    the_admin = admin_helper.read_one(id)
    return render_template('admin/component/admin_edit_overlay.jinja2', admin=the_admin)


@app.route('/_/templates/booking_edit', methods=['post'])
@login_required
def templates_booking_edit():
    id = request.form['id']
    the_booking = booking_helper.read_one(id)
    return render_template('admin/component/booking_edit_overlay.jinja2', booking=the_booking)


if __name__ == '__main__':
    app.run(debug=True)

import secrets

from flask import Flask
from sqlalchemy import create_engine
from flask_login import LoginManager

from flask_login import login_required, current_user

from admin import *
from organisasi import *
from authman import *

app = Flask(__name__)

engine = create_engine("sqlite:///serbaguna.db")

# Generate security key https://stackoverflow.com/a/54433731
app.config['SECRET_KEY'] = secrets.token_urlsafe(32)  # Python >= 3.6

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


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


@app.route('/admin/booking')
@login_required
def admin_booking_view():
    """
    Halaman admin bagian booking
    """
    pass


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


@login_manager.unauthorized_callback
def unauthorized():
    """
    Halaman yang di-redirect ketika tidak ada user yang login
    """
    # TODO: Buat halaman unauthorized?
    pass


@app.route('/')
def index_view():
    pass


if __name__ == '__main__':
    app.run()

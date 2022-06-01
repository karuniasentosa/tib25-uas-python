from sqlalchemy.engine import Engine

from werkzeug.security import generate_password_hash, \
                                check_password_hash

from flask_login import logout_user, login_user

from admin import AdminModel, AdminHelper


class AuthMan:
    """
    Class utility yang mengatur Otorisasi (login, logout, registrasi)
    dan session
    """
    @staticmethod
    def login(engine: Engine, username, password):
        the_admin: AdminModel  # buat variabel terlebih dahulu

        with AdminHelper(engine) as helper:
            the_admin = helper.read_one(username)  # minta cari admin berdasarkan username

        if the_admin is None:  # langsung return False jika tidak ditemukan
            return False

        password_hash = the_admin.password  # dapatkan password hash dari the_admin
        password_correct = check_password_hash(password_hash, password)

        if password_correct:
            return login_user(the_admin)
        else:
            return False

    @staticmethod
    def logout():
        logout_user()
        pass

    @staticmethod
    def register(engine: Engine, username, password):
        new_admin: AdminModel = AdminModel()
        new_admin.username = username
        new_admin.password = generate_password_hash(password)
        with AdminHelper(engine) as helper:
            helper.create(new_admin)



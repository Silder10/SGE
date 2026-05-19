from flask import Flask, request, render_template
from extensions import db
from flask_login import LoginManager
from auth.routes import auth_bp
from events.routes import events_bp
from users.routes import users_bp
from models import Usuarios, Eventos, Registracion

app = Flask(__name__)

app.config['SECRET_KEY'] = 'clave_super_segura'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/sge'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SECURE'] = False
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

db.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(user_id):
    return Usuarios.query.get(int(user_id))

app.register_blueprint(auth_bp)
app.register_blueprint(events_bp)
app.register_blueprint(users_bp)

@app.route('/')
def inicio():
    return render_template('base.html')

@app.errorhandler(403)
def error_403(error):

    return render_template(
        '403.html'
    ), 403


@app.errorhandler(404)
def error_404(error):

    return render_template(
        '404.html'
    ), 404

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)

print("hola")

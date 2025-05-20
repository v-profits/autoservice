from flask import Flask, render_template
from models import db, User
from routes import create_routes

app = Flask(__name__)
app.secret_key = 'автосервис73'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.create_all()
    if not User.query.first():
        admin = User(username='admin', password='admin')
        db.session.add(admin)
        db.session.commit()

create_routes(app)

@app.route('/')
def index():
    return render_template('base.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)



# from flask import Flask, render_template
# from models import db
# from routes import create_routes
#
# app = Flask(__name__)
#
# app.secret_key = 'автосервис73'  #  ключ
#
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db.init_app(app)
#
# with app.app_context():
#     db.create_all()
#
# create_routes(app)
#
# @app.before_first_request
# def create_user():
#     if not User.query.first():
#         db.create_all()
#         admin = User(username='admin', password='admin')
#         db.session.add(admin)
#         db.session.commit()
#
#
# @app.route('/')
# def index():
#     return render_template('base.html')
#
# @app.errorhandler(404)
# def page_not_found(e):
#     return render_template('404.html'), 404
#
# if __name__ == '__main__':
#     # app.run(host='0.0.0.0', port=5000, debug=True)
#     app.run(host='0.0.0.0', port=5000)

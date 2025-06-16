import os
from flask import Flask, render_template
from models import db, User, Order
from routes import create_routes
from flask_sqlalchemy import SQLAlchemy
from flask import render_template_string

app = Flask(__name__)
app.secret_key = 'автосервис73'
basedir = os.path.abspath(os.path.dirname(__file__))

# папка под БД
db_dir = os.path.join(basedir, "data")
os.makedirs(db_dir, exist_ok=True)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(db_dir, "autoservice.db")

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()
    if not User.query.first():
        admin = User(username='admin', password='admin')
        db.session.add(admin)
        db.session.commit()

create_routes(app)

# Функция для формирования отчета по заказу
@app.route('/order_report/<int:order_id>')
def order_report(order_id):
    order = Order.query.get_or_404(order_id)
    vehicle = order.vehicle
    client = vehicle.client if vehicle else None

    # services - объекты OrderService, из них берем service.name и service.price
    services = order.services  # list of OrderService

    # employees - объекты OrderEmployee, из них берем employee.name
    employees = order.employees  # list of OrderEmployee

    total = sum(os.subtotal for os in services)

    services_html = ''.join(
        f'<li>{os.service.name} – {os.subtotal} ₽ (x{os.quantity})</li>' for os in services
    )
    employees_html = ''.join(
        f'<li>{oe.employee.name}</li>' for oe in employees
    )

    report_html = f"""
    <strong>Клиент:</strong> {client.name if client else 'Неизвестно'}<br>
    <strong>Автомобиль:</strong> {vehicle.make if vehicle else '---'} {vehicle.model if vehicle else ''} ({vehicle.registration_number if vehicle else ''})<br>
    <strong>Дата:</strong> {order.date_created}<br>
    <strong>Статус:</strong> {order.status}<br><br>

    <strong>Услуги:</strong><br>
    <ul>
        {services_html}
    </ul>

    <strong>Сотрудники:</strong><br>
    <ul>
        {employees_html}
    </ul>

    <strong>Итого:</strong> {total} ₽
    """

    return render_template_string(report_html)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

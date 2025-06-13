from flask_sqlalchemy import SQLAlchemy
from datetime import date

# Инициализация SQLAlchemy
db = SQLAlchemy()

class User(db.Model):
    """Модель пользователя системы"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)  # Логин
    password = db.Column(db.String(100), nullable=False)  # Пароль

class Client(db.Model):
    """Модель клиента автосервиса"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)  # ФИО клиента
    phone = db.Column(db.String(50))  # Телефон
    email = db.Column(db.String(100))  # Email
    description = db.Column(db.String(1000))  # Доп. информация

class Vehicle(db.Model):
    """Модель транспортного средства"""
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id', ondelete='CASCADE'), nullable=False)  # Владелец
    make = db.Column(db.String(50))  # Марка
    model = db.Column(db.String(50))  # Модель
    year = db.Column(db.String(10))  # Год выпуска
    registration_number = db.Column(db.String(20))  # Гос. номер
    vin = db.Column(db.String(100))  # VIN-код
    description = db.Column(db.String(1000))  # Доп. информация

    # Связь с клиентом
    client = db.relationship('Client', backref=db.backref('vehicles', lazy=True, cascade='all, delete-orphan'))

class Service(db.Model):
    """Модель услуги автосервиса"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)  # Название услуги
    price = db.Column(db.Float, nullable=False)  # Цена
    execution_date = db.Column(db.Date)  # Дата выполнения
    description = db.Column(db.String(1000))  # Описание

class Employee(db.Model):
    """Модель сотрудника автосервиса"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)  # ФИО сотрудника
    position = db.Column(db.String(100))  # Должность
    specialization = db.Column(db.String(100))  # Специализация
    description = db.Column(db.String(1000))  # Доп. информация

class Order(db.Model):
    """Модель заказа в автосервисе"""
    id = db.Column(db.Integer, primary_key=True)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.id', ondelete='CASCADE'), nullable=False)  # Транспортное средство
    date_created = db.Column(db.Date)  # Дата создания заказа
    status = db.Column(db.String(50))  # Статус заказа
    description = db.Column(db.String(1000))  # Описание

    # Связи с другими таблицами
    vehicle = db.relationship('Vehicle', backref=db.backref('orders', lazy=True, cascade='all, delete-orphan'))

    # Услуги в заказе
    services = db.relationship(
        'OrderService',
        backref='order',
        lazy=True,
        cascade='all, delete-orphan',
        passive_deletes=True
    )

    # Сотрудники, работающие над заказом
    employees = db.relationship(
        'OrderEmployee',
        backref='order',
        lazy=True,
        cascade='all, delete-orphan',
        passive_deletes=True
    )

class OrderService(db.Model):
    """Связь заказов и услуг (многие-ко-многим)"""
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id', ondelete='CASCADE'), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('service.id', ondelete='CASCADE'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)  # Количество
    subtotal = db.Column(db.Float, nullable=False)  # Сумма (цена * количество)

    service = db.relationship('Service')  # Связь с услугой

class OrderEmployee(db.Model):
    """Связь заказов и сотрудников (многие-ко-многим)"""
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id', ondelete='CASCADE'), nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id', ondelete='CASCADE'), nullable=False)

    employee = db.relationship('Employee')  # Связь с сотрудником

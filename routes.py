from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Order, Vehicle, OrderService, OrderEmployee, Service, Employee, Client
from datetime import date

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def create_routes(app):

    # ---------------------- КЛИЕНТЫ ----------------------
    @app.route('/clients')
    def clients():
        all_clients = Client.query.all()
        return render_template('clients.html', clients=all_clients)

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/add_client', methods=['GET', 'POST'])
    def add_client():
        if request.method == 'POST':
            name = request.form['name']
            phone = request.form['phone']
            email = request.form['email']
            description = request.form['description']
            new_client = Client(name=name, phone=phone, email=email, description=description)
            db.session.add(new_client)
            db.session.commit()
            return redirect(url_for('clients'))
        return render_template('add_client.html')

    @app.route('/edit_client/<int:id>', methods=['GET', 'POST'])
    def edit_client(id):
        client = Client.query.get_or_404(id)
        if request.method == 'POST':
            client.name = request.form['name']
            client.phone = request.form['phone']
            client.email = request.form['email']
            client.description = request.form['description']
            db.session.commit()
            return redirect(url_for('clients'))
        return render_template('edit_client.html', client=client)

    @app.route('/delete_client/<int:id>')
    def delete_client(id):
        client = Client.query.get_or_404(id)
        db.session.delete(client)
        db.session.commit()
        return redirect(url_for('clients'))

    # ---------------------- АВТОМОБИЛИ ----------------------
    @app.route('/vehicles')
    def vehicles():
        all_vehicles = Vehicle.query.all()
        return render_template('vehicles.html', vehicles=all_vehicles)

    @app.route('/add_vehicle', methods=['GET', 'POST'])
    def add_vehicle():
        if request.method == 'POST':
            client_id = request.form['client_id']
            make = request.form['make']
            model = request.form['model']
            year = request.form['year']
            registration_number = request.form['registration_number']
            vin = request.form['vin']
            description = request.form['description']
            new_vehicle = Vehicle(client_id=client_id, make=make, model=model, year=year, registration_number=registration_number,  vin=vin, description=description)
            db.session.add(new_vehicle)
            db.session.commit()
            return redirect(url_for('vehicles'))
        clients = Client.query.all()
        return render_template('add_vehicle.html', clients=clients)

    @app.route('/edit_vehicle/<int:id>', methods=['GET', 'POST'])
    def edit_vehicle(id):
        vehicle = Vehicle.query.get_or_404(id)
        if request.method == 'POST':
            vehicle.client_id = request.form['client_id']
            vehicle.make = request.form['make']
            vehicle.model = request.form['model']
            vehicle.year = request.form['year']
            vehicle.registration_number = request.form['registration_number']
            vehicle.vin = request.form['vin']
            vehicle.description = request.form['description']

            print("DEBUG: регистрационный номер:", request.form['registration_number'])
            print("DEBUG: до изменения:", vehicle.registration_number)

            db.session.commit()

            print("DEBUG: после изменения:", vehicle.registration_number)

            return redirect(url_for('vehicles'))

        clients = Client.query.all()
        return render_template('edit_vehicle.html', vehicle=vehicle, clients=clients)


    @app.route('/delete_vehicle/<int:id>')
    def delete_vehicle(id):
        vehicle = Vehicle.query.get_or_404(id)
        db.session.delete(vehicle)
        db.session.commit()
        return redirect(url_for('vehicles'))

    # ---------------------- УСЛУГИ ----------------------
    @app.route('/services')
    def services():
        all_services = Service.query.all()
        return render_template('services.html', services=all_services)

    @app.route('/add_service', methods=['GET', 'POST'])
    def add_service():
        if request.method == 'POST':
            name = request.form['name']
            price = float(request.form['price'])
            execution_date_str = request.form.get('execution_date')
            execution_date = datetime.strptime(execution_date_str, '%Y-%m-%d').date() if execution_date_str else None
            description = request.form['description']
            new_service = Service(name=name, price=price, execution_date=execution_date, description=description)
            db.session.add(new_service)
            db.session.commit()
            return redirect(url_for('services'))
        return render_template('add_service.html', service=None)


    @app.route('/edit_service/<int:id>', methods=['GET', 'POST'])
    def edit_service(id):
        service = Service.query.get_or_404(id)
        if request.method == 'POST':
            service.name = request.form['name']
            service.price = float(request.form['price'])
            execution_date_str = request.form.get('execution_date')
            service.execution_date = datetime.strptime(execution_date_str, '%Y-%m-%d').date() if execution_date_str else None
            service.description = request.form['description']
            db.session.commit()
            return redirect(url_for('services'))
        return render_template('edit_service.html', service=service)

    @app.route('/delete_service/<int:id>')
    def delete_service(id):
        service = Service.query.get_or_404(id)
        db.session.delete(service)
        db.session.commit()
        return redirect(url_for('services'))

    # ---------------------- СОТРУДНИКИ ----------------------
    @app.route('/employees')
    def employees():
        all_employees = Employee.query.all()
        return render_template('employees.html', employees=all_employees)

    @app.route('/add_employee', methods=['GET', 'POST'])
    def add_employee():
        if request.method == 'POST':
            name = request.form['name']
            position = request.form['position']
            specialization = request.form['specialization']
            description = request.form['description']
            new_employee = Employee(name=name, position=position, specialization=specialization, description=description)
            db.session.add(new_employee)
            db.session.commit()
            return redirect(url_for('employees'))
        return render_template('add_employee.html')

    @app.route('/edit_employee/<int:id>', methods=['GET', 'POST'])
    def edit_employee(id):
        employee = Employee.query.get_or_404(id)
        if request.method == 'POST':
            employee.name = request.form['name']
            employee.position = request.form['position']
            employee.specialization = request.form['specialization']
            employee.description = request.form['description']
            db.session.commit()
            return redirect(url_for('employees'))
        return render_template('edit_employee.html', employee=employee)

    @app.route('/delete_employee/<int:id>')
    def delete_employee(id):
        employee = Employee.query.get_or_404(id)
        db.session.delete(employee)
        db.session.commit()
        return redirect(url_for('employees'))

    # ---------------------- ЗАКАЗЫ ----------------------
    @app.route('/orders')
    def orders():
        all_orders = Order.query.all()
        return render_template('orders.html', orders=all_orders)

    @app.route('/add_order', methods=['GET', 'POST'])
    def add_order():
        if request.method == 'POST':
            vehicle_id = request.form['vehicle_id']
            date_created = datetime.strptime(request.form['date_created'], '%Y-%m-%d').date()
            status = request.form['status']
            description = request.form['description']
            new_order = Order(vehicle_id=vehicle_id, date_created=date_created, status=status, description=description)
            db.session.add(new_order)
            db.session.commit()
            return redirect(url_for('orders'))
        vehicles = Vehicle.query.all()
        return render_template('add_order.html', vehicles=vehicles)

    @app.route('/edit_order/<int:order_id>', methods=['GET', 'POST'])
    def edit_order(id):
        order = Order.query.get_or_404(id)
        if request.method == 'POST':
            order.date_created = datetime.strptime(request.form['date_created'], '%Y-%m-%d').date()
            order.status = request.form['status']
            order.description = request.form['description']
            db.session.commit()
            return redirect(url_for('orders'))
        return render_template('edit_order.html', order=order)

    @app.route('/orders/delete/<int:order_id>', methods=['POST'])
    def delete_order(order_id):
        # Удаляем связи с услугами
        OrderService.query.filter_by(order_id=order_id).delete()
        # Удаляем связи с сотрудниками
        OrderEmployee.query.filter_by(order_id=order_id).delete()
        # Удаляем сам заказ
        order = Order.query.get(order_id)
        if order:
            db.session.delete(order)
        db.session.commit()
        return redirect(url_for('orders'))


    # ---------------------- ДОБАВЛЕНИЕ УСЛУГ К ЗАКАЗУ ----------------------
    @app.route('/assign_service/<int:order_id>', methods=['GET', 'POST'])
    def assign_service(order_id):
        order = Order.query.get_or_404(order_id)
        if request.method == 'POST':
            service_id = request.form['service_id']
            quantity = int(request.form['quantity'])
            service = Service.query.get(service_id)
            subtotal = quantity * service.price
            assignment = OrderService(order_id=order.id, service_id=service_id, quantity=quantity, subtotal=subtotal)
            db.session.add(assignment)
            db.session.commit()
            return redirect(url_for('orders'))
        services = Service.query.all()
        return render_template('assign_service.html', order=order, services=services)

    # ---------------------- НАЗНАЧЕНИЕ СОТРУДНИКОВ ----------------------
    @app.route('/assign_employee/<int:order_id>', methods=['GET', 'POST'])
    def assign_employee(order_id):
        order = Order.query.get_or_404(order_id)
        if request.method == 'POST':
            employee_id = request.form['employee_id']
            assignment = OrderEmployee(order_id=order.id, employee_id=employee_id)
            db.session.add(assignment)
            db.session.commit()
            return redirect(url_for('orders'))
        employees = Employee.query.all()
        return render_template('assign_employee.html', order=order, employees=employees)

# Add your database models here

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    year = db.Column(db.String(10))
    vin = db.Column(db.String(50), unique=True)
    notes = db.Column(db.Text)
    company = db.Column(db.String(100))
    license_plate = db.Column(db.String(30))
    maintenance_logs = db.relationship('MaintenanceLog', backref='vehicle', lazy=True)

class MaintenanceLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(20))
    type = db.Column(db.String(50))
    description = db.Column(db.String(200))
    cost = db.Column(db.String(50))
    total = db.Column(db.String(50))
    notes = db.Column(db.String(200))
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.id'), nullable=False)

class Purchase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.id'), nullable=False)
    date = db.Column(db.String(20))
    description = db.Column(db.String(200))
    cost = db.Column(db.String(50))
    notes = db.Column(db.String(200))

class Part(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    stock = db.Column(db.Integer, default=0)
    cost = db.Column(db.String(50))
    notes = db.Column(db.String(200))

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

class Invoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    invoice_number = db.Column(db.String(50), unique=True, nullable=False)
    date = db.Column(db.String(20), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='unpaid')
    company = db.Column(db.String(100))
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.id'), nullable=True)
    file_path = db.Column(db.String(200))
    notes = db.Column(db.String(200))

    vehicle = db.relationship('Vehicle', backref='invoices', lazy=True)

class DriverInvoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    invoice_number = db.Column(db.String(50), unique=True, nullable=False)
    date = db.Column(db.String(20), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='unpaid')
    driver_id = db.Column(db.Integer, nullable=False)  # You can link to a Driver table if you have one
    file_path = db.Column(db.String(200))
    notes = db.Column(db.String(200))

class FleetOwnerInvoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    invoice_number = db.Column(db.String(50), unique=True, nullable=False)
    date = db.Column(db.String(20), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='unpaid')
    fleet_owner_id = db.Column(db.Integer, nullable=False)  # You can link to a FleetOwner table if you have one
    file_path = db.Column(db.String(200))
    notes = db.Column(db.String(200))

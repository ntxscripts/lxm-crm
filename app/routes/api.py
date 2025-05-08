from flask import Blueprint, jsonify, render_template, request, send_from_directory
from ..models import db, Vehicle, MaintenanceLog, Purchase, Part, User, DriverInvoice, FleetOwnerInvoice
from sqlalchemy import func
from werkzeug.security import generate_password_hash, check_password_hash
from .auth import login_required, admin_required
from datetime import datetime, timedelta
import os
from werkzeug.utils import secure_filename

api_bp = Blueprint('api', __name__)

UPLOAD_DRIVER_DIR = os.path.join(os.getcwd(), 'uploads', 'driver_invoices')
UPLOAD_FLEET_DIR = os.path.join(os.getcwd(), 'uploads', 'fleet_invoices')
os.makedirs(UPLOAD_DRIVER_DIR, exist_ok=True)
os.makedirs(UPLOAD_FLEET_DIR, exist_ok=True)

@api_bp.route('/')
@login_required
def home():
    return render_template('index.html')

@api_bp.route('/vehicles')
@login_required
def vehicles():
    return render_template('vehicles.html')

@api_bp.route('/maintenance')
@login_required
def maintenance():
    return render_template('maintenance.html')

@api_bp.route('/reports')
@login_required
def reports():
    return render_template('reports.html')

@api_bp.route('/parts')
@login_required
def parts():
    return render_template('parts.html')

@api_bp.route('/service_history')
@login_required
def service_history():
    return render_template('service_history.html')

@api_bp.route('/admin_settings')
@admin_required
def admin_settings():
    return render_template('admin_settings.html')

@api_bp.route('/purchases')
@login_required
def purchases():
    return render_template('purchases.html')

@api_bp.route('/driver_invoices')
@login_required
def driver_invoices():
    return render_template('driver_invoices.html')

@api_bp.route('/fleet_invoices')
@login_required
def fleet_invoices():
    return render_template('fleet_invoices.html')

@api_bp.route('/api/vehicles', methods=['GET'])
def api_get_vehicles():
    vehicles = Vehicle.query.all()
    return jsonify([{
        'id': v.id,
        'name': v.name,
        'year': v.year,
        'vin': v.vin,
        'license_plate': v.license_plate,
        'company': v.company,
        'notes': v.notes
    } for v in vehicles])

@api_bp.route('/api/vehicles', methods=['POST'])
def api_add_vehicle():
    data = request.json
    v = Vehicle(name=data['name'], year=data.get('year'), vin=data.get('vin'), license_plate=data.get('license_plate'), company=data.get('company'), notes=data.get('notes'))
    db.session.add(v)
    db.session.commit()
    return jsonify({'success': True, 'id': v.id})

@api_bp.route('/api/vehicles/<int:vehicle_id>', methods=['PUT'])
def api_edit_vehicle(vehicle_id):
    v = Vehicle.query.get_or_404(vehicle_id)
    data = request.json
    v.name = data.get('name', v.name)
    v.year = data.get('year', v.year)
    v.vin = data.get('vin', v.vin)
    v.license_plate = data.get('license_plate', v.license_plate)
    v.company = data.get('company', v.company)
    v.notes = data.get('notes', v.notes)
    db.session.commit()
    return jsonify({'success': True})

@api_bp.route('/api/vehicles/<int:vehicle_id>', methods=['DELETE'])
def api_delete_vehicle(vehicle_id):
    v = Vehicle.query.get_or_404(vehicle_id)
    db.session.delete(v)
    db.session.commit()
    return jsonify({'success': True})

@api_bp.route('/api/maintenance', methods=['GET'])
def api_get_maintenance():
    logs = MaintenanceLog.query.all()
    return jsonify([{
        'id': l.id,
        'date': l.date,
        'type': l.type,
        'description': l.description,
        'cost': l.cost,
        'total': l.total,
        'notes': l.notes,
        'vehicle_id': l.vehicle_id,
        'vehicle_name': l.vehicle.name if l.vehicle else None,
        'vehicle_company': l.vehicle.company if l.vehicle else None,
        'vehicle_license_plate': l.vehicle.license_plate if l.vehicle else None
    } for l in logs])

@api_bp.route('/api/maintenance', methods=['POST'])
def api_add_maintenance():
    data = request.json
    log = MaintenanceLog(
        date=data['date'],
        type=data['type'],
        description=data.get('description'),
        cost=data.get('cost'),
        total=data.get('total'),
        notes=data.get('notes'),
        vehicle_id=data['vehicle_id']
    )
    db.session.add(log)
    db.session.commit()
    return jsonify({'success': True, 'id': log.id})

@api_bp.route('/api/maintenance/<int:log_id>', methods=['PUT'])
def api_edit_maintenance(log_id):
    log = MaintenanceLog.query.get_or_404(log_id)
    data = request.json
    log.date = data.get('date', log.date)
    log.type = data.get('type', log.type)
    log.description = data.get('description', log.description)
    log.cost = data.get('cost', log.cost)
    log.total = data.get('total', log.total)
    log.notes = data.get('notes', log.notes)
    log.vehicle_id = data.get('vehicle_id', log.vehicle_id)
    db.session.commit()
    return jsonify({'success': True})

@api_bp.route('/api/maintenance/<int:log_id>', methods=['DELETE'])
def api_delete_maintenance(log_id):
    log = MaintenanceLog.query.get_or_404(log_id)
    db.session.delete(log)
    db.session.commit()
    return jsonify({'success': True})

@api_bp.route('/api/test')
def test():
    return jsonify({'message': 'LXM CRM backend up and running!'})

@api_bp.route('/api/purchases', methods=['GET'])
def api_get_purchases():
    logs = MaintenanceLog.query.all()
    return jsonify([{
        'id': l.id,
        'vehicle_id': l.vehicle_id,
        'vehicle_name': l.vehicle.name if l.vehicle else '',
        'vehicle_company': l.vehicle.company if l.vehicle else '',
        'vehicle_license_plate': l.vehicle.license_plate if l.vehicle else '',
        'date': l.date,
        'type': l.type,
        'description': l.description,
        'cost': l.cost,
        'total': l.total,
        'notes': l.notes
    } for l in logs])

@api_bp.route('/api/purchases', methods=['POST'])
def api_add_purchase():
    data = request.json
    purchase = Purchase(
        vehicle_id=data['vehicle_id'],
        date=data.get('date'),
        description=data.get('description'),
        cost=data.get('cost'),
        notes=data.get('notes')
    )
    db.session.add(purchase)
    db.session.commit()
    return jsonify({'success': True, 'id': purchase.id})

@api_bp.route('/api/purchases/<int:purchase_id>', methods=['PUT'])
def api_edit_purchase(purchase_id):
    purchase = Purchase.query.get_or_404(purchase_id)
    data = request.json
    purchase.vehicle_id = data.get('vehicle_id', purchase.vehicle_id)
    purchase.date = data.get('date', purchase.date)
    purchase.description = data.get('description', purchase.description)
    purchase.cost = data.get('cost', purchase.cost)
    purchase.notes = data.get('notes', purchase.notes)
    db.session.commit()
    return jsonify({'success': True})

@api_bp.route('/api/purchases/<int:purchase_id>', methods=['DELETE'])
def api_delete_purchase(purchase_id):
    purchase = Purchase.query.get_or_404(purchase_id)
    db.session.delete(purchase)
    db.session.commit()
    return jsonify({'success': True})

# API: Parts
@api_bp.route('/api/parts', methods=['GET'])
def api_get_parts():
    parts = Part.query.all()
    return jsonify([{
        'id': p.id,
        'name': p.name,
        'stock': p.stock,
        'cost': p.cost,
        'notes': p.notes
    } for p in parts])

@api_bp.route('/api/parts', methods=['POST'])
def api_add_part():
    data = request.json
    part = Part(name=data['name'], stock=data.get('stock', 0), cost=data.get('cost'), notes=data.get('notes'))
    db.session.add(part)
    db.session.commit()
    return jsonify({'success': True, 'id': part.id})

@api_bp.route('/api/parts/<int:part_id>', methods=['PUT'])
def api_edit_part(part_id):
    part = Part.query.get_or_404(part_id)
    data = request.json
    part.name = data.get('name', part.name)
    part.stock = data.get('stock', part.stock)
    part.cost = data.get('cost', part.cost)
    part.notes = data.get('notes', part.notes)
    db.session.commit()
    return jsonify({'success': True})

@api_bp.route('/api/parts/<int:part_id>', methods=['DELETE'])
def api_delete_part(part_id):
    part = Part.query.get_or_404(part_id)
    db.session.delete(part)
    db.session.commit()
    return jsonify({'success': True})

# API: Service History (CRUD)
@api_bp.route('/api/service_history', methods=['GET'])
def api_get_service_history():
    logs = MaintenanceLog.query.filter(func.lower(MaintenanceLog.type) == 'service').all()
    return jsonify([{
        'id': l.id,
        'vehicle_id': l.vehicle_id,
        'vehicle_name': l.vehicle.name if l.vehicle else None,
        'vehicle_company': l.vehicle.company if l.vehicle else None,
        'vehicle_license_plate': l.vehicle.license_plate if l.vehicle else None,
        'date': l.date,
        'type': l.type,
        'description': l.description,
        'cost': l.cost,
        'total': l.total,
        'notes': l.notes
    } for l in logs])

@api_bp.route('/api/service_history', methods=['POST'])
def api_add_service():
    data = request.json
    log = MaintenanceLog(
        date=data['date'],
        type='Service',
        description=data.get('description'),
        notes=data.get('notes'),
        vehicle_id=data['vehicle_id']
    )
    db.session.add(log)
    db.session.commit()
    return jsonify({'success': True, 'id': log.id})

@api_bp.route('/api/service_history/<int:log_id>', methods=['PUT'])
def api_edit_service(log_id):
    log = MaintenanceLog.query.get_or_404(log_id)
    data = request.json
    log.date = data.get('date', log.date)
    log.description = data.get('description', log.description)
    log.notes = data.get('notes', log.notes)
    log.vehicle_id = data.get('vehicle_id', log.vehicle_id)
    db.session.commit()
    return jsonify({'success': True})

@api_bp.route('/api/service_history/<int:log_id>', methods=['DELETE'])
def api_delete_service(log_id):
    log = MaintenanceLog.query.get_or_404(log_id)
    db.session.delete(log)
    db.session.commit()
    return jsonify({'success': True})

# API: Users (CRUD) - Admin only
@api_bp.route('/api/users', methods=['GET'])
@admin_required
def api_get_users():
    users = User.query.all()
    return jsonify([{
        'id': u.id,
        'username': u.username,
        'is_admin': u.is_admin
    } for u in users])

@api_bp.route('/api/users', methods=['POST'])
@admin_required
def api_add_user():
    data = request.json
    user = User(
        username=data['username'],
        password_hash=generate_password_hash(data['password']),
        is_admin=data.get('is_admin', False)
    )
    db.session.add(user)
    db.session.commit()
    return jsonify({'success': True, 'id': user.id})

@api_bp.route('/api/users/<int:user_id>', methods=['PUT'])
@admin_required
def api_edit_user(user_id):
    user = User.query.get_or_404(user_id)
    data = request.json
    if 'password' in data and data['password']:
        user.password_hash = generate_password_hash(data['password'])
    if 'is_admin' in data:
        user.is_admin = data['is_admin']
    db.session.commit()
    return jsonify({'success': True})

@api_bp.route('/api/users/<int:user_id>', methods=['DELETE'])
@admin_required
def api_delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'success': True})

@api_bp.route('/api/dashboard', methods=['GET'])
def api_dashboard():
    total_vehicles = Vehicle.query.count()
    pending_maintenance = MaintenanceLog.query.count()
    # Sum all costs in MaintenanceLog as total cost
    total_cost = 0.0
    for log in MaintenanceLog.query.all():
        try:
            total_cost += float(str(log.cost).replace(',', '').replace('$', ''))
        except:
            pass
    for part in Part.query.all():
        try:
            total_cost += float(str(part.cost).replace(',', '').replace('$', ''))
        except:
            pass
    upcoming_services = MaintenanceLog.query.filter(MaintenanceLog.type == 'Service').count()

    # Recent activity: get last 5 changes from all tables
    recent = []
    for v in Vehicle.query.order_by(Vehicle.id.desc()).limit(2):
        recent.append({'type': 'Vehicle', 'action': 'Added', 'desc': v.name, 'time': v.id})
    for m in MaintenanceLog.query.order_by(MaintenanceLog.id.desc()).limit(2):
        recent.append({'type': 'Maintenance', 'action': m.type, 'desc': m.description or '', 'time': m.id})
    for p in Purchase.query.order_by(Purchase.id.desc()).limit(1):
        recent.append({'type': 'Purchase', 'action': 'Added', 'desc': p.description or '', 'time': p.id})
    for part in Part.query.order_by(Part.id.desc()).limit(1):
        recent.append({'type': 'Part', 'action': 'Added', 'desc': part.name, 'time': part.id})
    recent = sorted(recent, key=lambda x: x['time'], reverse=True)[:5]

    return jsonify({
        'total_vehicles': total_vehicles,
        'pending_maintenance': pending_maintenance,
        'total_cost': '' if total_cost == 0 else total_cost,
        'upcoming_services': upcoming_services,
        'recent_activity': recent
    })

@api_bp.route('/api/reports/data')
@login_required
def api_reports_data():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    # Base query for maintenance logs
    query = MaintenanceLog.query
    
    # Apply date filters if provided
    if start_date:
        query = query.filter(MaintenanceLog.date >= datetime.strptime(start_date, '%Y-%m-%d'))
    if end_date:
        query = query.filter(MaintenanceLog.date <= datetime.strptime(end_date, '%Y-%m-%d'))
    
    logs = query.all()
    
    # Calculate vehicle costs
    vehicle_costs = {}
    for log in logs:
        if log.vehicle_id not in vehicle_costs:
            vehicle_costs[log.vehicle_id] = 0
        vehicle_costs[log.vehicle_id] += log.cost
    
    # Get vehicle details
    vehicles = Vehicle.query.filter(Vehicle.id.in_(vehicle_costs.keys())).all()
    vehicle_costs_data = [
        {
            'name': v.name,
            'cost': vehicle_costs[v.id]
        }
        for v in vehicles
    ]
    
    # Calculate service types
    service_types = {}
    for log in logs:
        if log.service_type not in service_types:
            service_types[log.service_type] = 0
        service_types[log.service_type] += 1
    
    service_types_data = [
        {
            'type': service_type,
            'count': count
        }
        for service_type, count in service_types.items()
    ]
    
    # Calculate monthly trends
    monthly_costs = {}
    for log in logs:
        month_key = log.date.strftime('%Y-%m')
        if month_key not in monthly_costs:
            monthly_costs[month_key] = 0
        monthly_costs[month_key] += log.cost
    
    monthly_trend_data = [
        {
            'month': month,
            'cost': cost
        }
        for month, cost in sorted(monthly_costs.items())
    ]
    
    # Calculate company distribution
    company_counts = {}
    for log in logs:
        if log.vehicle.company not in company_counts:
            company_counts[log.vehicle.company] = 0
        company_counts[log.vehicle.company] += 1
    
    company_dist_data = [
        {
            'company': company,
            'count': count
        }
        for company, count in company_counts.items()
    ]
    
    # Calculate cost breakdown (parts vs labor)
    parts_cost = sum(log.cost for log in logs if log.service_type == 'Parts')
    labor_cost = sum(log.cost for log in logs if log.service_type != 'Parts')
    
    # Calculate vehicle utilization
    vehicle_utilization = {}
    total_days = (datetime.now() - min(log.date for log in logs)).days if logs else 0
    for log in logs:
        if log.vehicle_id not in vehicle_utilization:
            vehicle_utilization[log.vehicle_id] = 0
        vehicle_utilization[log.vehicle_id] += 1
    
    vehicle_utilization_data = [
        {
            'name': v.name,
            'utilization': min(100, (count / total_days * 100) if total_days > 0 else 0)
        }
        for v in vehicles
        for count in [vehicle_utilization.get(v.id, 0)]
    ]
    
    # Calculate cost per mile
    total_miles = sum(v.mileage for v in vehicles)
    cost_per_mile = sum(vehicle_costs.values()) / total_miles if total_miles > 0 else 0
    
    # Calculate average utilization
    avg_utilization = sum(u['utilization'] for u in vehicle_utilization_data) / len(vehicle_utilization_data) if vehicle_utilization_data else 0
    
    # Generate predictive maintenance data
    upcoming_services = []
    for vehicle in vehicles:
        # Get last service date for each service type
        last_services = {}
        for log in logs:
            if log.vehicle_id == vehicle.id and log.service_type not in last_services:
                last_services[log.service_type] = log.date
        
        # Predict next service based on service type
        for service_type, last_date in last_services.items():
            days_since_service = (datetime.now() - last_date).days
            service_interval = {
                'Oil Change': 90,
                'Tire Rotation': 180,
                'Brake Service': 365,
                'Inspection': 180,
                'Parts': 365
            }.get(service_type, 180)
            
            days_until_due = service_interval - days_since_service
            if days_until_due <= 30:  # Only show services due within 30 days
                priority = 'high' if days_until_due <= 7 else 'medium' if days_until_due <= 14 else 'low'
                upcoming_services.append({
                    'vehicle_name': vehicle.name,
                    'description': f'Next {service_type} due',
                    'due_date': (last_date + timedelta(days=service_interval)).strftime('%Y-%m-%d'),
                    'priority': priority,
                    'estimated_cost': '$100'  # This could be made more sophisticated
                })
    
    # Sort upcoming services by due date
    upcoming_services.sort(key=lambda x: x['due_date'])
    
    # Generate maintenance timeline
    maintenance_timeline = [
        {
            'date': log.date.strftime('%Y-%m-%d'),
            'vehicle_name': log.vehicle.name,
            'description': log.description,
            'type': log.service_type,
            'cost': f'${log.cost}'
        }
        for log in sorted(logs, key=lambda x: x.date, reverse=True)
    ]
    
    # Generate detailed reports
    reports = [
        {
            'id': 'maintenance',
            'type': 'Maintenance Report',
            'dateRange': f'{start_date} to {end_date}',
            'totalCost': sum(vehicle_costs.values()),
            'totalServices': len(logs)
        },
        {
            'id': 'cost',
            'type': 'Cost Analysis',
            'dateRange': f'{start_date} to {end_date}',
            'totalCost': sum(vehicle_costs.values()),
            'totalServices': len(logs)
        },
        {
            'id': 'utilization',
            'type': 'Utilization Report',
            'dateRange': f'{start_date} to {end_date}',
            'totalCost': 0,
            'totalServices': len(vehicle_utilization_data)
        }
    ]
    
    return jsonify({
        'vehicleCosts': vehicle_costs_data,
        'serviceTypes': service_types_data,
        'monthlyTrend': monthly_trend_data,
        'companyDist': company_dist_data,
        'partsCost': parts_cost,
        'laborCost': labor_cost,
        'vehicleUtilization': vehicle_utilization_data,
        'costPerMile': cost_per_mile,
        'avgUtilization': round(avg_utilization, 1),
        'totalVehicles': len(vehicles),
        'totalCost': sum(vehicle_costs.values()),
        'totalServices': len(logs),
        'activeCompanies': len(company_counts),
        'upcomingServices': upcoming_services,
        'maintenanceTimeline': maintenance_timeline,
        'reports': reports
    })

# --- DriverInvoice Endpoints ---
@api_bp.route('/api/driver_invoices', methods=['GET'])
def api_get_driver_invoices():
    invoices = DriverInvoice.query.all()
    return jsonify([{
        'id': i.id,
        'invoice_number': i.invoice_number,
        'date': i.date,
        'amount': i.amount,
        'status': i.status,
        'driver_id': i.driver_id,
        'file_path': i.file_path,
        'notes': i.notes
    } for i in invoices])

@api_bp.route('/api/driver_invoices', methods=['POST'])
def api_add_driver_invoice():
    data = request.form
    file = request.files.get('file')
    file_path = None
    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join('uploads/driver_invoices', filename)
        file.save(os.path.join(UPLOAD_DRIVER_DIR, filename))
    invoice = DriverInvoice(
        invoice_number=data['invoice_number'],
        date=data['date'],
        amount=float(data['amount']),
        status=data.get('status', 'unpaid'),
        driver_id=int(data['driver_id']),
        file_path=file_path,
        notes=data.get('notes')
    )
    db.session.add(invoice)
    db.session.commit()
    return jsonify({'success': True, 'id': invoice.id})

@api_bp.route('/api/driver_invoices/<int:invoice_id>', methods=['PUT'])
def api_edit_driver_invoice(invoice_id):
    invoice = DriverInvoice.query.get_or_404(invoice_id)
    data = request.form
    file = request.files.get('file')
    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join('uploads/driver_invoices', filename)
        file.save(os.path.join(UPLOAD_DRIVER_DIR, filename))
        invoice.file_path = file_path
    invoice.invoice_number = data.get('invoice_number', invoice.invoice_number)
    invoice.date = data.get('date', invoice.date)
    invoice.amount = float(data.get('amount', invoice.amount))
    invoice.status = data.get('status', invoice.status)
    invoice.driver_id = int(data.get('driver_id', invoice.driver_id))
    invoice.notes = data.get('notes', invoice.notes)
    db.session.commit()
    return jsonify({'success': True})

@api_bp.route('/api/driver_invoices/<int:invoice_id>', methods=['DELETE'])
def api_delete_driver_invoice(invoice_id):
    invoice = DriverInvoice.query.get_or_404(invoice_id)
    db.session.delete(invoice)
    db.session.commit()
    return jsonify({'success': True})

@api_bp.route('/api/driver_invoices/file/<filename>', methods=['GET'])
def api_get_driver_invoice_file(filename):
    return send_from_directory(UPLOAD_DRIVER_DIR, filename)

# --- FleetOwnerInvoice Endpoints ---
@api_bp.route('/api/fleet_invoices', methods=['GET'])
def api_get_fleet_invoices():
    invoices = FleetOwnerInvoice.query.all()
    return jsonify([{
        'id': i.id,
        'invoice_number': i.invoice_number,
        'date': i.date,
        'amount': i.amount,
        'status': i.status,
        'fleet_owner_id': i.fleet_owner_id,
        'file_path': i.file_path,
        'notes': i.notes
    } for i in invoices])

@api_bp.route('/api/fleet_invoices', methods=['POST'])
def api_add_fleet_invoice():
    data = request.form
    file = request.files.get('file')
    file_path = None
    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join('uploads/fleet_invoices', filename)
        file.save(os.path.join(UPLOAD_FLEET_DIR, filename))
    invoice = FleetOwnerInvoice(
        invoice_number=data['invoice_number'],
        date=data['date'],
        amount=float(data['amount']),
        status=data.get('status', 'unpaid'),
        fleet_owner_id=int(data['fleet_owner_id']),
        file_path=file_path,
        notes=data.get('notes')
    )
    db.session.add(invoice)
    db.session.commit()
    return jsonify({'success': True, 'id': invoice.id})

@api_bp.route('/api/fleet_invoices/<int:invoice_id>', methods=['PUT'])
def api_edit_fleet_invoice(invoice_id):
    invoice = FleetOwnerInvoice.query.get_or_404(invoice_id)
    data = request.form
    file = request.files.get('file')
    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join('uploads/fleet_invoices', filename)
        file.save(os.path.join(UPLOAD_FLEET_DIR, filename))
        invoice.file_path = file_path
    invoice.invoice_number = data.get('invoice_number', invoice.invoice_number)
    invoice.date = data.get('date', invoice.date)
    invoice.amount = float(data.get('amount', invoice.amount))
    invoice.status = data.get('status', invoice.status)
    invoice.fleet_owner_id = int(data.get('fleet_owner_id', invoice.fleet_owner_id))
    invoice.notes = data.get('notes', invoice.notes)
    db.session.commit()
    return jsonify({'success': True})

@api_bp.route('/api/fleet_invoices/<int:invoice_id>', methods=['DELETE'])
def api_delete_fleet_invoice(invoice_id):
    invoice = FleetOwnerInvoice.query.get_or_404(invoice_id)
    db.session.delete(invoice)
    db.session.commit()
    return jsonify({'success': True})

@api_bp.route('/api/fleet_invoices/file/<filename>', methods=['GET'])
def api_get_fleet_invoice_file(filename):
    return send_from_directory(UPLOAD_FLEET_DIR, filename)

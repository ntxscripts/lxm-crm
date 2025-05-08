from flask import Blueprint, request, jsonify, session, redirect, url_for, render_template, current_app
from ..models import db, User
from werkzeug.security import check_password_hash
from functools import wraps

auth_bp = Blueprint('auth', __name__)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        user = User.query.get(session['user_id'])
        if not user or not user.is_admin:
            return jsonify({'success': False, 'message': 'Admin access required'}), 403
        return f(*args, **kwargs)
    return decorated_function

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    
    data = request.json
    current_app.logger.info(f"Login attempt for username: {data.get('username')}")
    
    user = User.query.filter_by(username=data['username']).first()
    if not user:
        current_app.logger.warning(f"User not found: {data.get('username')}")
        return jsonify({'success': False, 'message': 'Invalid username or password'}), 401
    
    if check_password_hash(user.password_hash, data['password']):
        session['user_id'] = user.id
        session['is_admin'] = user.is_admin
        current_app.logger.info(f"Login successful for user: {user.username}")
        return jsonify({'success': True})
    
    current_app.logger.warning(f"Invalid password for user: {user.username}")
    return jsonify({'success': False, 'message': 'Invalid username or password'}), 401

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))

@auth_bp.route('/check_auth')
def check_auth():
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        return jsonify({
            'authenticated': True,
            'is_admin': user.is_admin if user else False
        })
    return jsonify({'authenticated': False}) 
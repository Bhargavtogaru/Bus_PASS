from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime, timedelta
from app import app, db
from models import User, BusPass
import uuid

# Authentication routes
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('user_dashboard' if not user.is_admin else 'admin_dashboard'))
        flash('Invalid username or password')
    
    return render_template('auth/login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if password != confirm_password:
            flash('Passwords do not match')
            return render_template('auth/register.html')
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists')
            return render_template('auth/register.html')
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered')
            return render_template('auth/register.html')
        
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please login.')
        return redirect(url_for('login'))
    
    return render_template('auth/register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

# User routes
@app.route('/dashboard')
@login_required
def user_dashboard():
    if current_user.is_admin:
        return redirect(url_for('admin_dashboard'))
    passes = BusPass.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard/user_dashboard.html', passes=passes)

@app.route('/apply-pass', methods=['POST'])
@login_required
def apply_pass():
    pass_type = request.form.get('pass_type')
    
    # Calculate expiry date based on pass type
    if pass_type == 'monthly':
        expiry_date = datetime.utcnow() + timedelta(days=30)
    elif pass_type == 'quarterly':
        expiry_date = datetime.utcnow() + timedelta(days=90)
    elif pass_type == 'yearly':
        expiry_date = datetime.utcnow() + timedelta(days=365)
    else:
        flash('Invalid pass type')
        return redirect(url_for('user_dashboard'))
    
    # Generate unique pass number
    pass_number = f'BP{uuid.uuid4().hex[:8].upper()}'
    
    bus_pass = BusPass(
        pass_number=pass_number,
        expiry_date=expiry_date,
        user_id=current_user.id
    )
    
    db.session.add(bus_pass)
    db.session.commit()
    
    flash('Pass application submitted successfully')
    return redirect(url_for('user_dashboard'))

# Admin routes
@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        return redirect(url_for('user_dashboard'))
    
    users = User.query.filter_by(is_admin=False).all()
    passes = BusPass.query.order_by(BusPass.issue_date.desc()).limit(10).all()
    return render_template('dashboard/admin_dashboard.html', users=users, passes=passes)

@app.route('/admin/user/<int:user_id>/deactivate', methods=['POST'])
@login_required
def deactivate_user(user_id):
    if not current_user.is_admin:
        return jsonify({'success': False, 'message': 'Unauthorized'})
    
    user = User.query.get_or_404(user_id)
    if user.is_admin:
        return jsonify({'success': False, 'message': 'Cannot deactivate admin user'})
    
    # Deactivate all active passes
    for bus_pass in user.passes:
        if bus_pass.status == 'active':
            bus_pass.status = 'deactivated'
    
    db.session.commit()
    return jsonify({'success': True})

@app.route('/admin/pass/<int:pass_id>/<action>', methods=['POST'])
@login_required
def manage_pass(pass_id, action):
    if not current_user.is_admin:
        return jsonify({'success': False, 'message': 'Unauthorized'})
    
    bus_pass = BusPass.query.get_or_404(pass_id)
    
    if action == 'approve':
        bus_pass.status = 'active'
        message = 'Pass approved successfully'
    elif action == 'reject':
        bus_pass.status = 'rejected'
        message = 'Pass rejected successfully'
    else:
        return jsonify({'success': False, 'message': 'Invalid action'})
    
    db.session.commit()
    return jsonify({'success': True, 'message': message})
from datetime import datetime
from flask import render_template, redirect, url_for, flash, request
from app import app, db
from app.forms import RegistrationForm, LoginForm, SendSMSForm
from app.models import User, SMSLog
from flask_login import login_user, current_user, logout_user, login_required
import requests
from app.tasks import send_scheduled_sms

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Account created successfully!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.password == form.password.data:
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('Login failed. Check your email and password.', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/send_sms', methods=['GET', 'POST'])
@login_required
def send_sms():
    form = SendSMSForm()
    if form.validate_on_submit():
        schedule_time = request.form.get('schedule_time')
        if schedule_time:
            # Schedule SMS
            schedule_time = datetime.strptime(schedule_time, '%Y-%m-%dT%H:%M')
            send_scheduled_sms.apply_async(args=[form.recipient.data, form.message.data], eta=schedule_time)
            flash('SMS scheduled successfully!', 'success')
        else:
            # Send SMS immediately via Kannel
            url = "http://localhost:13013/cgi-bin/sendsms"
            params = {
                'username': 'user',
                'password': 'pass',
                'to': form.recipient.data,
                'text': form.message.data
            }
            response = requests.get(url, params=params)
            if response.status_code == 202:
                flash('SMS sent successfully!', 'success')
            else:
                flash('Failed to send SMS.', 'danger')
    return render_template('send_sms.html', form=form)

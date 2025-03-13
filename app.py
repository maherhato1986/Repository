from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "your_secret_key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='technician')

class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(200), nullable=False)
    date = db.Column(db.String(20), nullable=False)
    num_elevators = db.Column(db.Integer, nullable=False)
    elevator_details = db.Column(db.Text, nullable=False)
    maintenance_checklists = db.Column(db.Text, nullable=False)
    technician_notes = db.Column(db.Text, nullable=True)
    recommendations = db.Column(db.Text, nullable=True)
    recipient_name = db.Column(db.String(100), nullable=False)
    submitted_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

@app.route('/')
def index():
    return redirect(url_for('submit_report'))

@app.route('/submit_report', methods=['GET', 'POST'])
def submit_report():
    maintenance_items = {
        "TRACTION القير المحرك": ["Wire Rope - الحبال", "Motor - الماتور", "Brake - البريك", "Rotary Encoder - الانكودر"],
        "CONTROL PANEL الكنترول": ["Relay - ريليه", "Printed Circuit Board - كروت الكنترول"],
        "DOORS الابواب": ["Cleanliness - نظافة الابواب", "Close Deceleration - الحركة في الاغلاق", "Opening Deceleration - الحركة في الفتح", "Contacts - الكوناتور", "Pin Contacts - دبوس الكنتاكتور", "Door Safety Edge - امان الباب", "Roller - ريلي الباب", "Light Curtain - حساس الباب"],
        "CABINE": ["STATUS - حالة الكبية من الداخل", "Cleanliness - نظافة الكبينه"],
        "C.O.P": ["Push Button - ازرار المبين الداخلي", "Key Switch - مفتاح اليوتش", "Card Key - كرت المبين الداخلي"],
        "RAILS": ["Guide Shoe - حشوات السكه", "Guide Roller - بكرة", "Bracket - البريك"],
        "SAFETY": ["Governor Switch - مفتاح السيفتي", "UPS - نظام الطوارى", "Limit Switches - ليمت سوتش"],
        "CARTOP": ["Cleanliness - نظافة فوق الكبينه", "Oiler Box - علبة المزايت", "Cartop Controller - كروت فوق الكبينه", "SMP - تحكم انسبكشن فوق الكبينه"],
        "PIT": ["Cleanliness - نظافة البئر", "Service Light - انارة البئر", "Fire Man Switch - مفتاح الحريق بالبئر", "Buffer - امان داخل البئر"]
    }
    
    if request.method == 'POST':
        project_name = request.form['project_name']
        location = request.form['location']
        date = request.form['date']
        num_elevators = int(request.form['num_elevators'])
        elevator_details = []
        maintenance_checklists = []
        
        for i in range(1, num_elevators + 1):
            elevator_details.append({
                "name": request.form[f'elevator_name_{i}'],
                "type": request.form[f'elevator_type_{i}'],
                "number": request.form[f'elevator_number_{i}']
            })
            checklist = request.form.getlist(f'maintenance_items_{i}')
            maintenance_checklists.append({
                "elevator": f"Elevator {i}",
                "checklist": checklist
            })
        
        technician_notes = request.form['technician_notes']
        recommendations = request.form['recommendations']
        recipient_name = request.form['recipient_name']
        report = Report(
            project_name=project_name,
            location=location,
            date=date,
            num_elevators=num_elevators,
            elevator_details=str(elevator_details),
            maintenance_checklists=str(maintenance_checklists),
            technician_notes=technician_notes,
            recommendations=recommendations,
            recipient_name=recipient_name,
            submitted_by=1  # Example user ID
        )
        db.session.add(report)
        db.session.commit()
        flash("Report submitted successfully!", "success")
        return redirect(url_for('submit_report'))
    return render_template('submit_report.html', maintenance_items=maintenance_items)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

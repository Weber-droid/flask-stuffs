from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your_secret_key')
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static/uploads')
app.config['ALLOWED_EXTENSIONS'] = {'pdf', 'doc', 'docx'}
db = SQLAlchemy(app)
migrate = Migrate(app, db)

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    location = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(120), nullable=False)

class PrintingProvider(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name_of_shop = db.Column(db.String(120), nullable=False)
    location = db.Column(db.String(120), nullable=False)
    phone_number = db.Column(db.String(20), unique=True, nullable=False)
    working_days = db.Column(db.String(120), nullable=False)
    services_provided = db.Column(db.String(250), nullable=False)
    password = db.Column(db.String(120), nullable=False)

class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(120), nullable=False)
    
    provider_id = db.Column(db.Integer, db.ForeignKey('printing_provider.id'), nullable=False)
    number_of_copies = db.Column(db.Integer, nullable=False)
    front_and_back = db.Column(db.Boolean, nullable=False)
    binding = db.Column(db.Boolean, nullable=False)
    student = db.relationship('Student', backref=db.backref('documents', lazy=True))
    provider = db.relationship('PrintingProvider', backref=db.backref('documents', lazy=True))
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/sign_up')
def sign_up():
    return render_template('sign_up.html')

@app.route('/signup_student', methods=['GET', 'POST'])
def signup_student():
    if request.method == 'POST':
        email = request.form['email']
        location = request.form['location']
        password = generate_password_hash(request.form['password'])
        
        new_student = Student(email=email, location=location, password=password)
        db.session.add(new_student)
        db.session.commit()
        
        # flash('Student signed up successfully!')
        return redirect(url_for('login_student'))
    
    return render_template('signup_student.html')

@app.route('/signup_printingprovider', methods=['GET', 'POST'])
def signup_printingprovider():
    if request.method == 'POST':
        name_of_shop = request.form['name_of_shop']
        location = request.form['location']
        phone_number = request.form['phone_number']
        working_days = ', '.join(request.form.getlist('working_days'))
        services_provided = ', '.join(request.form.getlist('services_provided'))
        password = generate_password_hash(request.form['password'])
        
        new_provider = PrintingProvider(
            name_of_shop=name_of_shop,
            location=location,
            phone_number=phone_number,
            working_days=working_days,
            services_provided=services_provided,
            password=password
        )
        db.session.add(new_provider)
        db.session.commit()
        
        # flash('Printing Provider signed up successfully!')
        return redirect(url_for('login_printingprovider'))
    
    return render_template('signup_printingprovider.html')

@app.route('/login_student', methods=['GET', 'POST'])
def login_student():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        student = Student.query.filter_by(email=email).first()
        
        if student and check_password_hash(student.password, password):
            session['student_id'] = student.id
            flash('Logged in successfully!')
            return redirect(url_for('student_home'))
        else:
            flash('Invalid email or password')
    
    return render_template('login_student.html')

@app.route('/login_printingprovider', methods=['GET', 'POST'])
def login_printingprovider():
    if request.method == 'POST':
        phone_number = request.form['phone_number']
        password = request.form['password']
        provider = PrintingProvider.query.filter_by(phone_number=phone_number).first()
        
        if provider and check_password_hash(provider.password, password):
            session['provider_id'] = provider.id
            flash('Logged in successfully!')
            return redirect(url_for('provider_dashboard', provider_id=provider.id))
        else:
            flash('Invalid phone number or password')
    
    return render_template('login_printingprovider.html')

@app.route('/student')
def student_home():
    if 'student_id' not in session:
        flash('Please log in first')
        return redirect(url_for('login_student'))
    return render_template('open_student.html')

@app.route('/submit_document', methods=['GET', 'POST'])
def submit_document():
    if 'student_id' not in session:
        flash('Please log in first')
        return redirect(url_for('login_student'))
    
    providers = PrintingProvider.query.all()
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            student_id = session['student_id']
            provider_id = request.form['provider_id']
            number_of_copies = request.form['number_of_copies']
            front_and_back = 'front_and_back' in request.form
            binding = 'binding' in request.form

            document = Document(
                filename=filename,
                student_id=student_id,
                provider_id=provider_id,
                number_of_copies=number_of_copies,
                front_and_back=front_and_back,
                binding=binding
            )
            db.session.add(document)
            db.session.commit()

            flash('Document submitted successfully!')
            return redirect(url_for('home'))

    return render_template('submit_document.html', providers=providers)

@app.route('/provider_dashboard/<int:provider_id>')
def provider_dashboard(provider_id):
    if 'provider_id' not in session or session['provider_id'] != provider_id:
        flash('Please log in first')
        return redirect(url_for('login_printingprovider'))
    
    provider = PrintingProvider.query.get_or_404(provider_id)
    documents = provider.documents
    return render_template('provider_dashboard.html', provider=provider, documents=documents)

@app.route('/graphic_designing')
def gd():
    return "<h1> Stay tuned for services related to graphic designing </h1>"

@app.route('/payment')
def payment():
    return render_template('payment.html')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

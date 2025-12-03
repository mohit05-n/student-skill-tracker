from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db
from models import Student, Skill, Certification, Course
from forms import LoginForm, RegistrationForm, StudentForm, EditProfileForm, CertificationForm
from datetime import datetime

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        student = Student.query.filter_by(username=form.username.data).first()
        if student and student.check_password(form.password.data):
            login_user(student, remember=form.remember_me.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('dashboard'))
        flash('Invalid username or password', 'danger')
    
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        # Check if username already exists
        if Student.query.filter_by(username=form.username.data).first():
            flash('Username already exists. Please choose a different one.', 'danger')
            return render_template('register.html', form=form)
        
        # Check if email already exists
        if Student.query.filter_by(email=form.email.data).first():
            flash('Email already registered. Please use a different email.', 'danger')
            return render_template('register.html', form=form)
        
        student = Student(username=form.username.data, email=form.email.data)
        student.set_password(form.password.data)
        db.session.add(student)
        db.session.commit()
        
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html', form=form)

@app.route('/dashboard')
@login_required
def dashboard():
    students_count = Student.query.count()
    skills_count = Skill.query.count()
    certifications_count = Certification.query.count()
    recent_students = Student.query.order_by(Student.created_at.desc()).limit(5).all()
    
    return render_template('dashboard.html', 
                         students_count=students_count,
                         skills_count=skills_count,
                         certifications_count=certifications_count,
                         recent_students=recent_students)

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', student=current_user)

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    
    if form.validate_on_submit():
        # Check if username is taken by another user
        existing_user = Student.query.filter_by(username=form.username.data).first()
        if existing_user and existing_user.id != current_user.id:
            flash('Username already taken. Please choose a different one.', 'danger')
            return render_template('profile.html', form=form)
        
        # Check if email is taken by another user
        existing_email = Student.query.filter_by(email=form.email.data).first()
        if existing_email and existing_email.id != current_user.id:
            flash('Email already taken. Please use a different email.', 'danger')
            return render_template('profile.html', form=form)
        
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.bio = form.bio.data
        
        # Update skills
        current_user.skills.clear()
        for skill_id in form.skills.data:
            skill = Skill.query.get(skill_id)
            if skill:
                current_user.skills.append(skill)
        
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('profile'))
    
    # Pre-populate form with current user data
    if request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.bio.data = current_user.bio
        form.skills.data = [skill.id for skill in current_user.skills]
    
    return render_template('profile.html', form=form, edit_mode=True)

@app.route('/add_student', methods=['GET', 'POST'])
@login_required
def add_student():
    form = StudentForm()
    
    if form.validate_on_submit():
        # Check if username already exists
        if Student.query.filter_by(username=form.username.data).first():
            flash('Username already exists. Please choose a different one.', 'danger')
            return render_template('add_student.html', form=form)
        
        # Check if email already exists
        if Student.query.filter_by(email=form.email.data).first():
            flash('Email already registered. Please use a different email.', 'danger')
            return render_template('add_student.html', form=form)
        
        student = Student(
            username=form.username.data,
            email=form.email.data,
            bio=form.bio.data
        )
        student.set_password(form.password.data)
        
        # Add selected skills
        for skill_id in form.skills.data:
            skill = Skill.query.get(skill_id)
            if skill:
                student.skills.append(skill)
        
        db.session.add(student)
        db.session.commit()
        
        flash('Student added successfully!', 'success')
        return redirect(url_for('view_students'))
    
    return render_template('add_student.html', form=form)

@app.route('/view_students')
@login_required
def view_students():
    page = request.args.get('page', 1, type=int)
    students = Student.query.paginate(
        page=page, per_page=10, error_out=False
    )
    return render_template('view_students.html', students=students)

@app.route('/student/<int:id>')
@login_required
def student_detail(id):
    student = Student.query.get_or_404(id)
    return render_template('student_form.html', student=student)

@app.route('/skills_by_course')
@login_required
def skills_by_course():
    courses = {}
    skills = Skill.query.all()
    
    for skill in skills:
        if skill.course not in courses:
            courses[skill.course] = []
        courses[skill.course].append(skill)
    
    return render_template('skills_by_course.html', courses=courses)

@app.route('/add_certification', methods=['GET', 'POST'])
@login_required
def add_certification():
    form = CertificationForm()
    
    if form.validate_on_submit():
        certification = Certification(
            name=form.name.data,
            issuer=form.issuer.data,
            issue_date=form.issue_date.data,
            expiry_date=form.expiry_date.data,
            credential_id=form.credential_id.data,
            student_id=current_user.id
        )
        
        db.session.add(certification)
        db.session.commit()
        
        flash('Certification added successfully!', 'success')
        return redirect(url_for('profile'))
    
    return render_template('add_student.html', form=form, title='Add Certification')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))

# Initialize default data
def create_default_data():
    # Create default skills if they don't exist
    default_skills = [
        {'name': 'Python', 'course': 'Programming', 'description': 'Python programming language'},
        {'name': 'Java', 'course': 'Programming', 'description': 'Java programming language'},
        {'name': 'JavaScript', 'course': 'Web Development', 'description': 'JavaScript programming language'},
        {'name': 'HTML/CSS', 'course': 'Web Development', 'description': 'Frontend web technologies'},
        {'name': 'SQL', 'course': 'Database', 'description': 'Structured Query Language'},
        {'name': 'React', 'course': 'Web Development', 'description': 'React JavaScript library'},
        {'name': 'Django', 'course': 'Web Development', 'description': 'Django web framework'},
        {'name': 'Machine Learning', 'course': 'Data Science', 'description': 'ML algorithms and techniques'},
        {'name': 'Data Analysis', 'course': 'Data Science', 'description': 'Data analysis techniques'},
        {'name': 'Leadership', 'course': 'Soft Skills', 'description': 'Leadership and management skills'},
        {'name': 'Communication', 'course': 'Soft Skills', 'description': 'Communication and presentation skills'},
    ]
    
    for skill_data in default_skills:
        if not Skill.query.filter_by(name=skill_data['name']).first():
            skill = Skill(**skill_data)
            db.session.add(skill)
    
    # Create default courses
    default_courses = [
        {'name': 'Programming', 'description': 'Core programming languages and concepts'},
        {'name': 'Web Development', 'description': 'Frontend and backend web development'},
        {'name': 'Database', 'description': 'Database design and management'},
        {'name': 'Data Science', 'description': 'Data analysis and machine learning'},
        {'name': 'Soft Skills', 'description': 'Communication and leadership skills'},
    ]
    
    for course_data in default_courses:
        if not Course.query.filter_by(name=course_data['name']).first():
            course = Course(**course_data)
            db.session.add(course)
    
    db.session.commit()

from flask import Flask, render_template, jsonify, request, flash, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, DateField, IntegerField, TextAreaField
from wtforms.validators import DataRequired
from sqlalchemy import inspect 
from sqlalchemy import create_engine, Column, Integer, ForeignKey, TIMESTAMP, String, Text, DECIMAL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime
from wtforms import Form, FieldList, FormField
from sqlalchemy import or_, desc
from sqlalchemy.orm import aliased
  


# Initialize the app and configurations
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users_states_data_base.db'
app.config['SECRET_KEY'] = "hada is my secret key for empty db"

db = SQLAlchemy(app)

# Flask_Login Stuff

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(id):
    return freelancers.query.get(int(id))

@app.context_processor
def base():
    form = GlobalSearchForm()
    return dict(form=form)



# Form Classes
class Signiniu_client_Form(FlaskForm):
    email = StringField("Email: ", validators=[DataRequired()])
    password = PasswordField('Password: ', validators=[DataRequired()])
    firstname = StringField("First name: ", validators=[DataRequired()])
    lastname = StringField('Last name: ', validators=[DataRequired()])
    address = StringField("Address: ", validators=[DataRequired()])
    phone_num = StringField('Phone number: ', validators=[DataRequired()])
    company = StringField("Company: ", validators=[DataRequired()])
    geneder = StringField('Gender: ', validators=[DataRequired()])
    birthdate = DateField("Birth date: ", validators=[DataRequired()], format='%Y-%m-%d')    
    submit = SubmitField("Submit")

class Signiniu_freelancer_Form(FlaskForm):
    email = StringField("Email: ", validators=[DataRequired()])
    password = PasswordField('Password: ', validators=[DataRequired()])
    firstname = StringField("First name: ", validators=[DataRequired()])
    lastname = StringField('Last name: ', validators=[DataRequired()])
    phone_num = StringField('Phone number: ', validators=[DataRequired()])
    succeces = IntegerField('Succece: ', validators=[DataRequired()])
    address = StringField("Address: ", validators=[DataRequired()])
    company = StringField("Company: ", validators=[DataRequired()])
    gender = StringField('Gender: ', validators=[DataRequired()])
    self_intro = TextAreaField("Profile description: ")
    profile_title = StringField("Profile title: ", validators=[DataRequired()])
    price_of_work_for_hour = IntegerField('price of work for hour: ', validators=[DataRequired()])

    birthdate = DateField("Birth date: ", validators=[DataRequired()], format='%Y-%m-%d')
    # skills = FieldList(FormField(SkillForm), min_entries=1, max_entries=10)  # Adjust max_entries as needed
    # experiencs = FieldList(FormField(experiencsForm), min_entries=1, max_entries=10)  # Adjust max_entries as needed
    submit = SubmitField("Submit")
  
class NamerForm(FlaskForm):
    name = StringField("What's Your Name", validators=[DataRequired()])
    submit = SubmitField("Submit")

class LoginForm(FlaskForm):
    email = StringField("Username or Email: ", validators=[DataRequired()])
    password = PasswordField("Password: ", validators=[DataRequired()])
    submit = SubmitField("Submit")

class deleteForm(FlaskForm):
    username = StringField("Username: ", validators=[DataRequired()])
    password = PasswordField("Password: ", validators=[DataRequired()])
    submit = SubmitField("Delete account")

class SigninForm(FlaskForm):
    username = StringField("Username: ", validators=[DataRequired()])
    password = PasswordField('Password: ', validators=[DataRequired()])
    submit = SubmitField("Submit")

class Check_Db_Formf(FlaskForm):
    username = StringField("Username: ", validators=[DataRequired()])
    submit = SubmitField("Submit")

class Delet_User_Form(FlaskForm):
    username = StringField("Use rname: ", validators=[DataRequired()])
    password = PasswordField('Password: ', validators=[DataRequired()])
    submit = SubmitField("Submit")

class updateForm(FlaskForm):
    skill_name = StringField("Skill Name", validators=[DataRequired()])
    proficiency_level = StringField("Proficiency Level", validators=[DataRequired()])
    experienc = StringField("Experienc:", validators=[DataRequired()])
    experienc_duration = StringField("experienc Duration:", validators=[DataRequired()])
    submit = SubmitField("Submit")

class jobForm(FlaskForm):
    title = StringField("Job Title", validators=[DataRequired()])
    description = TextAreaField("Job description: ")
    budget = IntegerField('budget: ', validators=[DataRequired()])
    location = StringField("Job lacation:", validators=[DataRequired()])
    submit = SubmitField("Submit")

class messageForm(FlaskForm):
    content = StringField("Youe message: ", validators=[DataRequired()])
    submit = SubmitField("Send")

class langaugForm(FlaskForm):
    langauge = StringField("langauge: ", validators=[DataRequired()])
    submit = SubmitField("add")

class SearchForm(FlaskForm):
    email = StringField("Youe searched: ", validators=[DataRequired()])
    search = SubmitField("Search")

class GlobalSearchForm(FlaskForm):
    searched = StringField("searched: ", validators=[DataRequired()])
    search = SubmitField("Search")

class skillsForm(FlaskForm):
    skill_name = StringField("skill: ", validators=[DataRequired()])
    submit = SubmitField("add")

class experiencForm(FlaskForm):
    experienc = StringField("experienc: ", validators=[DataRequired()])
    experienc_start_data = DateField("Start date: ", validators=[DataRequired()], format='%Y-%m-%d')
    experienc_end_data = DateField("end date: ", validators=[DataRequired()], format='%Y-%m-%d')
    submit = SubmitField("add")

class educationForm(FlaskForm):
    school = StringField("school: ", validators=[DataRequired()])
    sectore = StringField("sectore: ", validators=[DataRequired()])
    degree = StringField("degree: ", validators=[DataRequired()])
    date_start = DateField("start date: ", validators=[DataRequired()], format='%Y-%m-%d')
    date_end = DateField("end date: ", validators=[DataRequired()], format='%Y-%m-%d')
    submit = SubmitField("add")


class certificationForm(FlaskForm):
    certification = StringField("your ceritification: ", validators=[DataRequired()])
    certification_description = TextAreaField("certification description:")
    certification_url = StringField("your certification URL: ", validators=[DataRequired()])
    date_token = DateField("date token: ", validators=[DataRequired()], format='%Y-%m-%d')
    submit = SubmitField("add")



# Routes
@app.route('/', methods=['GET', 'POST'])
@login_required
def Test():

   
    current_freelancer = freelancers.query.filter_by(id = current_user.id).first()
    if current_freelancer:
        current_skills = Skills.query.filter_by(id=current_freelancer.id).all()
        jobs = []
        
        if current_skills:
            for skill in current_skills:
                s = skill.skill_name
                jobs += joboffers.query.filter(joboffers.description.like(f'%{s}%')).all()
        else:
            s = None
    else:
        flash('Freelancer profile not found.', 'error')
        return redirect(url_for('Test'))  # Redirect to homepage or appropriate route
    login = True
    home1 = True

    return render_template("home.html", jobs=jobs, String=s, login=login, home1=home1, user = current_freelancer)

@app.route('/wordlance/home/best_matches', methods=['GET', 'POST'])
@login_required
def home1():

    current_freelancer = freelancers.query.filter_by(id=current_user.id).first()
    
    if current_freelancer:
        current_skills = Skills.query.filter_by(id=current_freelancer.id).all()
        jobs = []
        
        if current_skills:
            for skill in current_skills:
                s = skill.skill_name
                jobs += joboffers.query.filter(joboffers.description.like(f'%{s}%')).all()
        else:
            s = None
    else:
        flash('Freelancer profile not found.', 'error')
        return redirect(url_for('index'))  # Redirect to homepage or appropriate route
    login = True
    home  = 1

    return render_template("home.html", jobs=jobs, String=s, login=login, home=home, user = current_freelancer)

@app.route('/wordlance/home/Most_recent', methods=['GET', 'POST'])
@login_required
def home2():  
    shpr = True
    current_freelancer = freelancers.query.filter_by(id=current_user.id).first()

    jobs = joboffers.query.order_by(desc(joboffers.date_posted)).all()
    login = True
    home = 2
    return render_template("home.html", shpr=shpr, jobs=jobs, login=login, home=home, user = current_freelancer)

@app.route('/wordlance/home/Saved_jobs', methods=['GET', 'POST'])
@login_required
def home3():
    shpr = True
    jobs = []
    saved_jobs_for_this_route = saved_jobs.query.filter_by(id=current_user.id).all()
    
    for saved_job in saved_jobs_for_this_route:
        job_offer = joboffers.query.filter_by(job_id=saved_job.job_id).first()
        if job_offer:
            jobs.append(job_offer)
        else:
            flash(f"Job offer with ID {saved_job.job_id} not found.", 'error')
    login = True
    home = 3
    current_freelancer = freelancers.query.filter_by(id=current_user.id).first()

    return render_template("home.html", shpr=shpr, jobs=jobs, login=login, home=home, user = current_freelancer)

@app.route('/save_job/<int:job_id>', methods=['POST', 'GET'])
@login_required
def save_job(job_id):
    new_saved_job = saved_jobs(job_id=job_id,id=current_user.id)
    db.session.add(new_saved_job)
    db.session.commit()
    flash("job Saved successfully!!")
    return redirect(url_for('home3'))

@app.route('/freelancer_application/<int:job_id>/<int:freelancer_id>', methods=['POST', 'GET'])
@login_required
def freelancer_application(job_id, freelancer_id):
    
    freelancer = freelancers.query.filter(freelancers.id == freelancer_id).first()

    new_application = applications(job_id=job_id,id=freelancer_id)
    db.session.add(new_application)
    db.session.commit()
    flash("Application registered successfully!")

    last_application = db.session.query(applications).order_by(applications.application_id.desc()).first()
    application_id_last =  last_application.application_id

    new_Submitted = Submitted(application_id=application_id_last,id=freelancer_id)
    db.session.add(new_Submitted)
    db.session.commit()
    flash("submitted registered successfully!")

    return redirect(url_for('Test'))

@app.route('/my_job_applications', methods=['GET', 'POST'])
@login_required
def my_job_applications():
    your_jobs = joboffers.query.filter(joboffers.id == current_user.id).all()
    client_info = clients.query.filter(clients.id == current_user.id).first()

    email = client_info.email
    firstname = client_info.firstname
    lastname = client_info.lastname
    address = client_info.address
    gender = client_info.gender
    birthdate = client_info.birthdate
   


    you_jobs_id = []
    for j in your_jobs:
        you_jobs_id.append(j.job_id)

    data = []

    for i in you_jobs_id:
        application_for_current_job = applications.query.filter(applications.job_id == i).all()
        for a in application_for_current_job:

            freelancer_email = freelancers.query.filter(freelancers.id == a.id ).first()
            email = freelancer_email.email

            mydict = {}
            mydict["job_id"]= a.job_id
            mydict["id"]= a.id
            mydict["applied_at"]= a.applied_at
            mydict["email"] = email

            data.append(mydict)
    login = True


    return render_template("myapplications.html",you_jobs_id=you_jobs_id, data = data,login=login,
  email=email,
            firstname=firstname, lastname=lastname, address=address, gender=gender, birthdate=birthdate)

@app.route('/jobs_i_apply_for', methods=['GET', 'POST'])
@login_required
def jobs_i_apply_for():
    my_applications = applications.query.filter(applications.id == current_user.id).all()
    if my_applications:
        for_free_lancer_id = applications.query.filter(applications.id == current_user.id).first()

        freelancer = freelancers.query.filter(freelancers.id == for_free_lancer_id.id).first()

        email = freelancer.email
        firstname = freelancer.firstname
        lastname = freelancer.lastname
        succeces = freelancer.succeces
        address = freelancer.address
        gender = freelancer.gender
        birthdate = freelancer.birthdate


        jobs_id_lists = []
        for a in my_applications:
            jobs_id_lists.append(a.job_id)

        data = []

        for i in jobs_id_lists:
            job = joboffers.query.filter(joboffers.job_id == i).first()
            mydict = {}
            mydict["job_id"]= job.job_id
            mydict["client_posted_id"]= job.id
            mydict["title"]= job.title
            mydict["description"]= job.description
            mydict["budget"]= job.budget
            mydict["location"]= job.location
            mydict["date_posted"]= job.date_posted

            data.append(mydict)


        login = True

        return render_template("jobs_i_apply_for.html", data = data, email=email,login = login,
            firstname=firstname, lastname=lastname,
            succeces=succeces, address=address, gender=gender, birthdate=birthdate)
    else:
        return render_template("jobs_i_apply_for.html")


@app.route('/search', methods=['GET', 'POST'])
@login_required
def Gloabalsearch():
    form = GlobalSearchForm()
    results = []
    if form.validate_on_submit():
        searched = form.searched.data

        # Search jobs by description, title, and location
        jobs = joboffers.query.filter(
            db.or_(
                joboffers.description.like('%' + searched + '%'),
                joboffers.title.like('%' + searched + '%'),
                joboffers.location.like('%' + searched + '%')
            )
        ).all()

        # Search clients by firstname, lastname, and email
        my_clients = clients.query.filter(
            db.or_(
                clients.firstname.like('%' + searched + '%'),
                clients.lastname.like('%' + searched + '%'),
                clients.email.like('%' + searched + '%')
            )
        ).all()

        # Search freelancers by firstname, lastname, email, self_intro, and profile_title
        my_freelancers = freelancers.query.filter(
            db.or_(
                freelancers.firstname.like('%' + searched + '%'),
                freelancers.lastname.like('%' + searched + '%'),
                freelancers.email.like('%' + searched + '%'),
                freelancers.self_intro.like('%' + searched + '%'),
                freelancers.profile_title.like('%' + searched + '%')
            )
        ).all()

        # Combine results into a single list with a consistent format
        for job in jobs:
            results.append({'type': 'Job', 'content': job.title})
        for client in my_clients:
            results.append({'type': 'Client', 'content': client.firstname + " " + client.lastname})
        for freelancer in my_freelancers:
            results.append({'type': 'Freelancer', 'content': freelancer.firstname + " " + freelancer.lastname})

        # Sort the combined list alphabetically by the 'content' key
        results.sort(key=lambda x: x['content'])

        return render_template("search.html", form=form, searched=searched, results=results)

    return render_template("search.html", form=form, results=results)

# Note: Make sure the model names and field names are accurate based on your actual models.




@app.route('/remove_job/<int:id>/<int:job_id>', methods=['GET', 'POST'])
@login_required
def remove_job(id, job_id):
    # Correct spelling of 'application'
    application = applications.query.filter_by(job_id=job_id, id=id).first()
    
    # Check if application exists
    if not application:
        flash("Application not found.")
        return redirect(url_for('jobs_i_apply_for'))
    
    # Get the job to remove or 404 if it doesn't exist
    job_to_remove = applications.query.get_or_404(application.application_id)
    
    try:
        db.session.delete(job_to_remove)
        db.session.commit()
        flash("Job removed successfully!")
    except Exception as e:
        db.session.rollback()
        flash("Whoops! Something went wrong: {}".format(e))
    
    return redirect(url_for('jobs_i_apply_for'))




@app.route('/update_user/<int:id>/<int:foc>', methods=['GET', 'POST'])
@login_required
def update(id, foc):

    skillsFormhtml = skillsForm()
    experienceFormhmtl = experiencForm()
    langaugFormhtml = langaugForm()
    educationFormhtml = educationForm()
    certificationFormhtml = certificationForm()

    current_skills = Skills.query.filter(Skills.id == current_user.id).all()
    current_experiencs = experiencs.query.filter(experiencs.id == current_user.id).all()
    current_langauges = langauges.query.filter(langauges.id == current_user.id).all()
    current_education = education.query.filter(education.id == current_user.id).all()

    current_certifications = Certifications2.query.filter(Certifications2.freelancer_id == current_user.id).all()

    if foc==1:
        user_to_update = freelancers.query.get_or_404(id)

    if skillsFormhtml.validate_on_submit():
        new_skill = Skills(id=user_to_update.id, 
                            skill_name=skillsFormhtml.skill_name.data,
                                        )
        db.session.add(new_skill)
        db.session.commit()
        skillsFormhtml.skill_name.data = ""
        flash(f"skill add successfully! for the user with the username: {user_to_update.email}")
        return redirect(url_for('my_profile', user_id = current_user.id))



    if experienceFormhmtl.validate_on_submit():
        new_experienc = experiencs(id=user_to_update.id, 
                            experienc=experienceFormhmtl.experienc.data,
                            experienc_start_data=experienceFormhmtl.experienc_start_data.data,
                            experienc_end_data=experienceFormhmtl.experienc_end_data.data
                                        )
        db.session.add(new_experienc)
        db.session.commit()
        experienceFormhmtl.experienc.data = ""
        experienceFormhmtl.experienc_start_data.data = ""
        experienceFormhmtl.experienc_end_data.data = ""
        flash(f"experienc add successfully! for the user with the username: {user_to_update.email}")
        return redirect(url_for('my_profile', user_id = current_user.id))

    
    if langaugFormhtml.validate_on_submit():
        new_langauge = langauges(id=user_to_update.id, 
                            langauge=langaugFormhtml.langauge.data)
        db.session.add(new_langauge)
        db.session.commit()
        langaugFormhtml.langauge.data=""
        flash(f"langauge add successfully! for the user with the username: {user_to_update.email}")
        return redirect(url_for('my_profile', user_id = current_user.id))

    
    if educationFormhtml.validate_on_submit():
        new_education = education(id=user_to_update.id, 
                            school = educationFormhtml.school.data,
                            sectore = educationFormhtml.sectore.data,
                            degree = educationFormhtml.degree.data,
                            date_start = educationFormhtml.date_start.data,
                            date_end = educationFormhtml.date_end.data)
        db.session.add(new_education)
        db.session.commit()
        educationFormhtml.school.data = ""
        educationFormhtml.sectore.data =""
        educationFormhtml.degree.data = ""
        flash(f"education add successfully! for the user with the username: {user_to_update.email}")
        return redirect(url_for('my_profile', user_id = current_user.id))


    if certificationFormhtml.validate_on_submit():
        new_certification = Certifications2(
            freelancer_id=user_to_update.id,
            certification=certificationFormhtml.certification.data,
            certification_description=certificationFormhtml.certification_description.data,
            certification_url=certificationFormhtml.certification_url.data,
            date_token=certificationFormhtml.date_token.data
        )
        db.session.add(new_certification)
        db.session.commit()
        certificationFormhtml.certification.data = ""
        certificationFormhtml.certification_description.data = ""
        certificationFormhtml.certification_url.data = ""
        certificationFormhtml.date_token.data = ""
        flash(f"Certification added successfully for the user with the username: {user_to_update.email}")
        return redirect(url_for('my_profile', user_id = current_user.id))



    login = True


    return render_template("update.html", skillsForm=skillsFormhtml, 
        experiencForm=experienceFormhmtl, 
        langaugForm=langaugFormhtml, 
        educationForm=educationFormhtml, 
        user_to_update=user_to_update,
        certificationForm = certificationFormhtml,
        login=login,
        current_skills=current_skills,
        current_experiencs=current_experiencs,
        current_langauges=current_langauges,
        current_education=current_education,
        current_certifications=current_certifications
        )

@app.route('/add_langauges/', methods=['GET', 'POST'])
@login_required
def add_langauge():
    user = freelancers.query.get_or_404(current_user.id)
    form = langaugForm()
    if form.validate_on_submit():
        new_langauge = langauges(id=user.id, 
                            langauge=form.langauge.data                                       )
        db.session.add(new_langauge)
        db.session.commit()
        flash(f"langaugge:{form.langauge.data} registered successfully!")
        return redirect(url_for('my_profile', user_id=current_user.id))
    login = True
    return render_template("langauge.html", form=form,login=login)

@app.route('/add_education/', methods=['GET', 'POST'])
@login_required
def add_education():
    user = freelancers.query.get_or_404(current_user.id)
    form = educationForm()
    if form.validate_on_submit():
        new_education = education(id=user.id, 
                            school = form.school.data,
                            sectore = form.sectore.data,
                            degree = form.degree.data,
                            date_start = form.date_start.data,
                            date_end = form.date_end.data)
        db.session.add(new_education)
        db.session.commit()
        flash(f"education:{form.sectore.data} registered successfully!")
        return redirect(url_for('my_profile', user_id=current_user.id))
    login = True
    return render_template("education.html", form=form,login=login)

@app.route('/delet_skill/<int:id>', methods=['GET', 'POST'])
@login_required
def delet_skill(id):
    skill_to_delet = Skills.query.get_or_404(id)
    try:
        db.session.delete(skill_to_delet)
        db.session.commit()
        flash(f"skill deleted successfully!")
    except:
        flash("whoops! somthing went worng.")
    login = True
    return redirect(url_for('update', id=current_user.id, foc =1) )

@app.route('/delet_langauge/<int:id>', methods=['GET', 'POST'])
@login_required
def delet_langauge(id):

    langauge_to_delet = langauges.query.get_or_404(id)
    try:
        db.session.delete(langauge_to_delet)
        db.session.commit()
        flash(f"langauge deleted successfully!")
    except:
        flash("whoops! somthing went worng.")
    login = True
    return redirect(url_for('update', id=current_user.id, foc =1) )

@app.route('/delet_experienc/<int:id>', methods=['GET', 'POST'])
@login_required
def dele_experience(id):
    experience_to_delet = experiencs.query.get_or_404(id)
    try:
        db.session.delete(experience_to_delet)
        db.session.commit()
        flash(f"experienc deleted successfully!")
    except:
        flash("whoops! somthing went worng.")    
    login = True
    return redirect(url_for('update', id=current_user.id, foc =1) )

@app.route('/delet_education/<int:id>', methods=['GET', 'POST'])
@login_required
def delet_educaiton(id):
    education_to_delet = education.query.get_or_404(id)
    try:
        db.session.delete(education_to_delet)
        db.session.commit()
        flash(f"education deleted successfully!")
    except:
        flash("whoops! somthing went worng.")    
    login = True
    return redirect(url_for('update', id=current_user.id, foc =1) )








@app.route('/job_inforamtion/<int:job_id>', methods=['GET', 'POST'])
@login_required
def job_inforamtion(job_id):
    job = joboffers.query.get_or_404(job_id)
    
    login = True
    return render_template("job_inforamtion.html", job = job,
    login=login)





@app.route('/delet_ceretificaion/<int:id>', methods=['GET', 'POST'])
@login_required
def delet_certificaiton(id):
    certificaion_to_delet = Certifications2.query.get_or_404(id)
    try:
        db.session.delete(certificaion_to_delet)
        db.session.commit()
        flash(f"Certification deleted successfully!")
    except:
        flash("whoops! somthing went worng.")    
    login = True
    return redirect(url_for('update', id=current_user.id, foc =1) )


#Create Job offer Page
@app.route('/job_offer/<int:id>/', methods=['GET', 'POST'])
@login_required
def job_offer(id):

    
    client_job = clients.query.get_or_404(id)

    form = jobForm()
    if form.validate_on_submit():


        new_job = joboffers(id=client_job.id, 
                            title=form.title.data,
                            description=form.description.data,
                            budget=form.budget.data,
                            location=form.location.data
                                        )

        db.session.add(new_job)
        db.session.commit()
        

        flash(f"Job offer registered successfully! for the Client with the username: {client_job.email}")

    login = True
    return render_template("joboffer.html", form=form,login=login)

@app.route('/my_profile/<int:user_id>', methods=['GET', 'POST'])
@login_required
def my_profile(user_id=1):
    user = freelancers.query.get_or_404(user_id)
    skills = Skills.query.filter(Skills.id == current_user.id ).all()
    my_education = education.query.filter(education.id == current_user.id ).all()
    my_experiencs = experiencs.query.filter(experiencs.id == current_user.id ).all()
    login = True
    mylangauges = langauges.query.filter(langauges.id == current_user.id)
    return render_template("profil.html", user = user, login=login, skills=skills, experiencs=my_experiencs, langauges=mylangauges, education=my_education)

@app.route('/send_message/<int:sender_client_id>/<int:receiver_client_id>', methods=['POST', 'GET'])
@login_required
def send_message(sender_client_id, receiver_client_id):

    form = messageForm()

    if form.validate_on_submit():
        content = form.content.data

        new_message = Message(sender_client_id=sender_client_id,receiver_client_id=receiver_client_id, content=content)
        db.session.add(new_message)
        db.session.commit()
    login = True
    return render_template("sendmessage.html", form=form, login=login)

@app.route('/my_messages', methods=['GET', 'POST'])
@login_required
def my_messages():
    form = SearchForm()
    id = current_user.id
    your_messages = Message.query.filter(Message.receiver_client_id == id or Message.sender_client_id == id).all()

    recievers_emails = []
    for m in your_messages:
        receiver = freelancers.query.filter(freelancers.id == m.receiver_client_id).first()
        recievers_emails.append(receiver)

    senders_emails = []
    for m in your_messages:
        sender = freelancers.query.filter(freelancers.id == m.sender_client_id).first()
        senders_emails.append(sender)

    thos_hwo_send_to_you = Message.query.filter(Message.receiver_client_id == current_user.id).all()
    thos_hwo_you_send_to = Message.query.filter(Message.sender_client_id == current_user.id).all()   

    users = []
    for m in thos_hwo_send_to_you:
        sender = freelancers.query.filter(freelancers.id == m.sender_client_id).first()
        users.append(sender)

    for m in thos_hwo_you_send_to:
        sender = freelancers.query.filter(freelancers.id == m.receiver_client_id).first()
        users.append(sender)

    for u in users:
        k = users.count(u)
        if k > 1:
            for i in range(k - 1):
                users.remove(u)

    login = True



    return render_template("my_messages.html", messages = your_messages,users=users, form=form, login=login,
        thos_hwo_send_to_you=thos_hwo_send_to_you,
        thos_hwo_you_send_to=thos_hwo_you_send_to
        )

@app.route('/convirsation/<int:receiver_id>', methods=['GET', 'POST'])
@login_required
def convirsation(receiver_id):
    form = messageForm()
    form2 = SearchForm()

    current_user_id = current_user.id

    if form.validate_on_submit():
        content = form.content.data
        form.content.data = ""

        new_message = Message(sender_client_id=current_user_id, receiver_client_id=receiver_id, content=content)
        db.session.add(new_message)
        db.session.commit()
    
    # Fetch messages between current user and the specified receiver
    messages_sent_to_receiver = Message.query.filter(
        (Message.sender_client_id == current_user_id) & 
        (Message.receiver_client_id == receiver_id)
    ).order_by(Message.date_posted).all()
    
    messages_received_from_receiver = Message.query.filter(
        (Message.sender_client_id == receiver_id) & 
        (Message.receiver_client_id == current_user_id)
    ).order_by(Message.date_posted).all()
    
    # Combine both lists of messages
    all_messages = messages_sent_to_receiver + messages_received_from_receiver
    
    # Create a dictionary for each message with necessary info
    messages_dict = []
    for m in all_messages:
        is_sender = 1 if m.sender_client_id == current_user_id else 0
        messages_dict.append({
            'content': m.content,
            'date_posted': m.date_posted,
            'is_sender': is_sender
        })

    # Sort the messages_dict list based on date_posted
    messages_dict.sort(key=lambda x: x['date_posted'])

    id = current_user.id
    thos_hwo_send_to_you = Message.query.filter(Message.receiver_client_id == current_user.id).all()
    thos_hwo_you_send_to = Message.query.filter(Message.sender_client_id == current_user.id).all()   

    users = []
    for m in thos_hwo_send_to_you:
        sender = freelancers.query.filter(freelancers.id == m.sender_client_id).first()
        users.append(sender)

    for m in thos_hwo_you_send_to:
        sender = freelancers.query.filter(freelancers.id == m.receiver_client_id).first()
        users.append(sender)

    user_connect_with_now = freelancers.query.filter(freelancers.id==receiver_id).first()

    for u in users:
        k = users.count(u)
        if k > 1:
            for i in range(k - 1):
                users.remove(u)

    login = True
    
    return render_template("convirsation.html", login=login, form2=form2, messages=messages_dict, form=form, users=users, receiver_id=receiver_id, user_connect_with_now=user_connect_with_now)

@app.route('/convirsation/search', methods=["POST"])
def search():
    form = SearchForm()
    users_search = freelancers.query
    if form.validate_on_submit():
        # Get data from submitted form
        email = form.email.data
        # Query the Database
        users_search = freelancers.query.filter(freelancers.email.like('%' + email + '%')).all()
        login = True
        return render_template("my_messages.html",
         form=form,
         search=search,
         users_search =  users_search,login=login )

@app.route('/apply_for_job/<int:job_id>', methods=['POST', 'GET'])
@login_required
def apply_for_job(job_id):

    try:
        new_application= applications(job_id=job_id,
                                        id=current_user.id)
        db.session.add(new_application)
        db.session.commit()
        flash("You had applied successfully!")
        return redirect(url_for('home1'))

    except:
        flash("somthing went wrong!!!")
        return redirect(url_for('home1'))




  


    
@app.route('/signin', methods=['GET', 'POST'])
def signin():
    
    client_form = Signiniu_client_Form()
    freelancer_form = Signiniu_freelancer_Form()
    if request.method == 'POST':

        client_or_freelancer = request.form.get('choice')
        if client_or_freelancer == 'client':

            flash('You selected Client. Please fill in the details.')
        elif client_or_freelancer == 'freelancer':

            flash('You selected Freelancer. Please fill in the details.')
    return render_template("Signin.html", client_form=client_form, freelancer_form=freelancer_form)

@app.route('/signin_client', methods=['POST'])
def signin_client():
    

    client_form = Signiniu_client_Form()
    if client_form.validate_on_submit():

        email = client_form.email.data
        password = client_form.password.data
        firstname = client_form.firstname.data
        lastname = client_form.lastname.data
        address = client_form.address.data
        phone_num = client_form.phone_num.data
        company = client_form.company.data
        gender = client_form.geneder.data
        birthdate = client_form.birthdate.data

        client = clients.query.filter_by(email=email).first()
        if not client:

            new_client = clients(   email=email, 
                                    password=password,
                                    firstname=firstname,
                                    lastname=lastname,
                                    address=address,
                                    phone_num=phone_num,
                                    company=company,
                                    gender=gender,
                                    birthdate=birthdate)
            db.session.add(new_client)
            db.session.commit()
            flash("Client registered successfully!")
            return redirect(url_for('login'))
        else:


            flash("Username already exists.")

    return redirect(url_for('signin'))

@app.route('/signin_freelancer', methods=['POST'])
def signin_freelancer():
    freelancer_form = Signiniu_freelancer_Form()
    if freelancer_form.validate_on_submit():

        email = freelancer_form.email.data
        password = freelancer_form.password.data
        firstname = freelancer_form.firstname.data
        lastname = freelancer_form.lastname.data
        phone_num = freelancer_form.phone_num.data
        succeces = freelancer_form.succeces.data
        address = freelancer_form.address.data
        gender = freelancer_form.gender.data
        birthdate = freelancer_form.birthdate.data
        company = freelancer_form.company.data
        self_intro = freelancer_form.self_intro.data
        profile_title = freelancer_form.profile_title.data
        price_of_work_for_hour = freelancer_form.price_of_work_for_hour.data
        flash("data reached backend successfully!!!")

        freealcer = freelancers.query.filter_by(email=email).first()
        if not freealcer:

            try:
                new_freelancer = freelancers(   email=email, 
                                        password=password,
                                        firstname=firstname,
                                        lastname=lastname,
                                        phone_num=phone_num,
                                        succeces=succeces,
                                        address=address,
                                        gender=gender,
                                        birthdate=birthdate,
                                        company=company,
                                        self_intro=self_intro,
                                        profile_title=profile_title,
                                        price_of_work_for_hour=price_of_work_for_hour
    )
                db.session.add(new_freelancer)
                db.session.commit()
                flash("Freelancer registered successfully!")
                return redirect(url_for('login'))
            except Exception as e:
                flash(f"there was an error on: {e}")
                return f"error is this shit: {e}"
        else:


            flash("Username already exists.")

    return redirect(url_for('signin'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Check if the user is a freelancer
        user = freelancers.query.filter_by(email=form.email.data).first()
        
        # If user not found among freelancers, check clients
        if not user:
            user = clients.query.filter_by(email=form.email.data).first()

        if user:
            if user.password == form.password.data:
                login_user(user)
                flash(f"Login Successful!your EMAIL is: {user.email}")

                return redirect(url_for('Test'))  # Replace 'Test' with your desired endpoint
            else:
                flash("Wrong Password - Try Again!")
        else:
            flash("That User Doesn't Exist! Try Again...")

    return render_template('Login.html', form=form)

# Create Logout Page
@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash("You Have Been Logged Out!  Thanks For Visiting Us...")
    return redirect(url_for('login'))

@app.route('/data', methods=['GET', 'POST'])
@login_required
def data():
    shpr = None
    clients_infos = clients.query.order_by(clients.date_created).all()
    freelancers_infos = freelancers.query.order_by(freelancers.date_created).all()
    skills  = Skills.query.order_by(Skills.id).all()
    Ex  = experiencs.query.order_by(experiencs.id).all()
    jo  = joboffers.query.order_by(joboffers.date_posted).all()

    if current_user.is_authenticated:
        shpr = True
    else:
        shpr = False
    current_user_email = current_user.email

    login = True

    return render_template("test.html",login=login, clients_infos = clients_infos, current_user_email=current_user_email, freelancers_infos=freelancers_infos, skills=skills, experiencs=Ex, jo=jo, shpr=shpr)

# Create Custom Error Pages ---  Invalid URL
@app.errorhandler(404)
def page_not_found(e):
	return render_template("404.html"), 404

# Internal Server Error
@app.errorhandler(500)
def page_not_found(e):
	return render_template("500.html"), 500


# Database Models
class clients(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)  # Adjusted for secure hashing
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(255))
    phone_num = db.Column(db.String(20), nullable=True)
    company = db.Column(db.String(50), nullable=True)
    gender = db.Column(db.String(20))
    birthdate = db.Column(db.Date)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)


class joboffers(db.Model):
    job_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id = db.Column(db.Integer, ForeignKey('clients.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    budget = db.Column(db.DECIMAL(10, 2))
    location = db.Column(db.String(100))
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)


class Skills(db.Model):
    skill_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    job_id = db.Column(db.Integer, ForeignKey('joboffers.job_id'), nullable=True)
    id = db.Column(db.Integer, ForeignKey('freelancers.id'), nullable=True)
    skill_name = db.Column(db.String(100), nullable=False)
    proficiency_level = db.Column(db.String(50), nullable=True)


class experiencs(db.Model):
    experienc_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id = db.Column(db.Integer, ForeignKey('freelancers.id'), nullable=False)
    experienc = db.Column(db.String(100), nullable=False)
    experienc_start_data = db.Column(db.Date)
    experienc_end_data = db.Column(db.Date)


class langauges(db.Model):
    langaug_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id = db.Column(db.Integer, ForeignKey('freelancers.id'), nullable=False)
    langauge = db.Column(db.String(100), nullable=False)

class education(db.Model):
    education_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id = db.Column(db.Integer, ForeignKey('freelancers.id'), nullable=False)
    school = db.Column(db.String(100), nullable=False)
    sectore = db.Column(db.String(100), nullable=False)
    degree = db.Column(db.String(100), nullable=False)    
    date_start = db.Column(db.Date)
    date_end = db.Column(db.Date)

class work(db.Model):
    word_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id = db.Column(db.Integer, ForeignKey('freelancers.id'), nullable=False)
    client_work_with = db.Column(db.Integer, ForeignKey('clients.id'), nullable=False)
    work_subject = db.Column(db.String(100), nullable=False)




class freelancers(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)  # Adjusted for secure hashing
    firstname = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    phone_num = db.Column(db.String(20), nullable=True)
    succeces = db.Column(db.Integer, nullable=True)
    address = db.Column(db.String(255))
    gender = db.Column(db.String(20))
    birthdate = db.Column(db.Date)
    company = db.Column(db.String(50), nullable=True)
    self_intro = db.Column(db.String(1000), nullable=False)
    profile_title = db.Column(db.String(50), nullable=False)
    price_of_work_for_hour = db.Column(db.Integer, nullable=True)

    date_created = db.Column(db.DateTime, default=datetime.utcnow)


class Message(db.Model):
    message_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sender_client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=True)
    receiver_client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=True)
    content = db.Column(db.Text)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)


class applications(db.Model):
    application_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    job_id = db.Column(db.Integer, ForeignKey('joboffers.job_id'), nullable=False)
    id = db.Column(db.Integer, ForeignKey('freelancers.id'), nullable=False)
    applied_at = db.Column(db.DateTime, default=datetime.utcnow)

class saved_jobs(db.Model):
    savd_job_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    job_id = db.Column(db.Integer, ForeignKey('joboffers.job_id'), nullable=False)
    id = db.Column(db.Integer, ForeignKey('freelancers.id'), nullable=False)


class Submitted(db.Model):
    submission_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    application_id =    db.Column(db.Integer, ForeignKey('applications.application_id'), nullable=False)
    id =                db.Column(db.Integer, ForeignKey('freelancers.id'), nullable=False)


    date_token = db.Column(db.DateTime, default=datetime.utcnow)

class Certifications2(db.Model):
    certification_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    freelancer_id = db.Column(db.Integer, db.ForeignKey('freelancers.id'), nullable=True)
    certification = db.Column(db.String(50),  nullable=False)
    certification_description = db.Column(db.Text)
    certification_url = db.Column(db.String(50),  nullable=False)
    date_token = db.Column(db.DateTime, default=datetime.utcnow)



# Create an application context and initialize the database
with app.app_context():
    db.create_all()

def print_all_tables():
    inspector = inspect(db.engine)
    tables = inspector.get_table_names()
    print("Tables in the database:")
    for table in tables:
        print(table)
    return "finish"





# # Function to drop the Users table
# def drop_users_table():
#     try:
#         Certifications2.__table__.drop(db.engine)
#         print("Table 'Certifications2' has been dropped.")
#     except Exception as e:
#         print(f"An error occurred: {e}")


# with app.app_context():
#     drop_users_table()



# if __name__ == '__main__':
#     with app.app_context():
#         print_all_tables()




# def delete_all_records():
#     try:
#         # Perform the deletion
#         db.session.query(Message).delete()
#         db.session.commit()
#         return 'All records deleted successfully!'
#     except Exception as e:
#         db.session.rollback()
#         return f'Error deleting records: {str(e)}'


# with app.app_context():
#     delete_all_records()


if __name__ == '__main__':
    app.run(debug=True)


    






from datetime import datetime

# Example function to add one row to each table
def add_sample_data():
    # Add a client
    client = clients(
        email="client@example.com",
        password="hashedpassword",
        firstname="John",
        lastname="Doe",
        address="123 Main St",
        phone_num="1234567890",
        company="Company Inc",
        gender="Male",
        birthdate=datetime(1985, 5, 20),
        date_created=datetime.utcnow()
    )
    db.session.add(client)
    db.session.commit()  # Commit to get the client.id

    # Add a freelancer
    freelancer = freelancers(
        email="freelancer@example.com",
        password="hashedpassword",
        firstname="Jane",
        lastname="Smith",
        phone_num="0987654321",
        succeces=5,
        address="456 Elm St",
        gender="Female",
        birthdate=datetime(1990, 7, 15),
        company="Freelance LLC",
        self_intro="Experienced freelancer.",
        profile_title="Graphic Designer",
        price_of_work_for_hour=30,
        date_created=datetime.utcnow()
    )
    db.session.add(freelancer)
    db.session.commit()  # Commit to get the freelancer.id

    # Add a job offer
    job_offer = joboffers(
        id=client.id,
        title="Web Development",
        description="Looking for a web developer to create a website.",
        budget=1500.00,
        location="Remote",
        date_posted=datetime.utcnow()
    )
    db.session.add(job_offer)
    db.session.commit()  # Commit to get the job_offer.job_id

    # Add a skill
    skill = Skills(
        job_id=job_offer.job_id,
        id=freelancer.id,
        skill_name="Python",
        proficiency_level="Expert"
    )
    db.session.add(skill)
    db.session.commit()

    # Add an experience
    experience = experiencs(
        id=freelancer.id,
        experienc="Software Development",
        experienc_start_data=datetime(2018, 1, 1),
        experienc_end_data=datetime(2020, 12, 31)
    )
    db.session.add(experience)
    db.session.commit()

    # Add a language
    language = langauges(
        id=freelancer.id,
        langauge="English"
    )
    db.session.add(language)
    db.session.commit()

    # Add an education
    education_entry = education(
        id=freelancer.id,
        school="University of Technology",
        sectore="Computer Science",
        degree="Bachelor's",
        date_start=datetime(2008, 9, 1),
        date_end=datetime(2012, 6, 30)
    )
    db.session.add(education_entry)
    db.session.commit()

    # Add a work entry
    work_entry = work(
        id=freelancer.id,
        client_work_with=client.id,
        work_subject="Web Design"
    )
    db.session.add(work_entry)
    db.session.commit()

    # Add a message
    message = Message(
        sender_client_id=client.id,
        receiver_client_id=client.id,
        content="Hello, this is a test message.",
        date_posted=datetime.utcnow()
    )
    db.session.add(message)
    db.session.commit()

    # Add an application
    application = applications(
        job_id=job_offer.job_id,
        id=freelancer.id,
        applied_at=datetime.utcnow()
    )
    db.session.add(application)
    db.session.commit()

    # Add a saved job
    saved_job = saved_jobs(
        job_id=job_offer.job_id,
        id=freelancer.id
    )
    db.session.add(saved_job)
    db.session.commit()

    # Add a submission
    submission = Submitted(
        application_id=application.application_id,
        id=freelancer.id
    )
  # Add a certification
    certification = certifications(
        freelancer_id=1,  # Replace with the appropriate freelancer_id
        certification="Certified Python Developer",
        certification_description="Certification for advanced proficiency in Python.",
        certification_url="https://example.com/certified-python-developer",
        date_token=datetime(2023, 7, 1)
    )
    db.session.add(certification)
    db.session.commit()
    print("Certification added successfully!")
    db.session.add(submission)
    db.session.commit()
    return "every goood . HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH..................EVERY THING IS GOOD!!!!!!!!!"
# 




# if __name__ == '__main__':
#     with app.app_context():
#         add_sample_data()














































































# # Function to drop the Users table
# def drop_users_table():
#     try:
#         Users.__table__.drop(db.engine)
#         print("Table 'users' has been dropped.")
#     except Exception as e:
#         print(f"An error occurred: {e}")


# with app.app_context():
#     drop_users_table()

# def print_all_tables():
#     inspector = inspect(db.engine)
#     tables = inspector.get_table_names()
#     print("Tables in the database:")
#     for table in tables:
#         print(table)
#     return "finish"

# if __name__ == '__main__':
#     with app.app_context():
#         print_all_tables()


# # Function to drop all tables
# def drop_all_tables():
#     db.reflect()
#     db.drop_all()
#     print("All tables have been dropped.")

# # Create an application context and drop all tables
# if __name__ == '__main__':
#     with app.app_context():
#         drop_all_tables()

# # Function to drop all tables
# def drop_all_tables():
#     db.reflect()
#     db.drop_all()
#     print("All tables have been dropped.")

# # Create an application context and drop all tables
# if __name__ == '__main__':
#     with app.app_context():
#         drop_all_tables()


# # Function to drop all tables
# def drop_all_tables():
#     db.reflect()
#     db.drop_all()
#     print("All tables have been dropped.")

# # Create an application context and drop all tables
# if __name__ == '__main__':
#     with app.app_context():
#         drop_all_tables()


# class users(db.Model, UserMixin):
#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     password = db.Column(db.String(120), nullable=False)
#     role = db.Column(db.String(20), nullable=False)  # 'client' or 'freelancer'

#     def get_id(self):
#         return str(self.id)  # Convert to string as required by Flask-Login

#     def __repr__(self):
#         return f'<User {self.email}>'

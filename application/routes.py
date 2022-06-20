from email.mime import image
import os
from io import BytesIO

from click import confirmation_option

from application import app, db, mail
from flask import render_template, url_for, request, flash, json, redirect, Response, session
from flask_mail import Message
from application.models import User, Projects, Gallery
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont



#Super User Creation:
if not(User.objects(user_id=1)):
    superuser   =   "Sooraj"
    password    =   "admin"
    
    user = User(user_id=1, user_name=superuser) 
    user.set_password(password)
    user.save()


#Gallery:
def imgGallery():
    if Gallery.objects.all().count() > 0: #Checking if there is images in DB
        images = Gallery.objects.all()
        return images
    else:
        return False
gallery = imgGallery()


#Recent Projects:
def recentProjects():
    if Projects.objects.all().count() == 0: #Checking if there is no projects in DB
        projectList = [False, False]
        return projectList
    if Projects.objects.all().count() < 4: #Checking if no. of projects are less than 3
        projects = Projects.objects.all()
    else:
        projects = Projects.objects.all().order_by('-id')[:3]
    imageList = []
    projectList = []
    for i in projects:
        projectImages = Gallery.objects.filter(project_name = i.project_name).first()
        imageList.append(projectImages)
    projectList.append(projects)
    projectList.append(imageList)
    return projectList
rProjects = recentProjects()
    

#Home Page:
@app.route("/")
@app.route("/index")
@app.route("/home")
def index():
    return render_template("index.html", gallery = imgGallery(), 
    rProjects = rProjects[0], imageList = rProjects[1], projectGallery_Flag = False)


#User Login:
@app.route("/login", methods = ['GET','POST'])
@app.route("/signin", methods = ['GET','POST'])
def login():
    if request.method == 'POST':
        user_name   =   request.form.get("name")
        password    =   request.form.get("password")
        user = User.objects(user_name = user_name).first()
        if user and user.get_password(password):
            session['login'] = True
            return redirect("/user")
        else:
            return render_template("login.html")
    else:
        return render_template("login.html")


#User LogOut:
@app.route("/logout")
@app.route("/signout")
def logout():
    session['login'] = False
    return redirect(url_for('index'))


#USER: Adding new Project:
@app.route("/user", methods = ['GET','POST'])
def users():
    if not session.get('login'):
        return redirect(url_for('login'))
    if request.method == 'GET':
        projectCounter = Projects.objects.all().count()
        if projectCounter == 0:
            return render_template("user.html", gallery = [],  
        projectCounter = projectCounter)
        else:
            print("rProjects[0].project_name =====",rProjects[0].project_name)
            return render_template("user.html", gallery = imgGallery(), 
            projectCounter = projectCounter, rProjects = rProjects[0], imageList = rProjects[1])
    else:
        if 'image' in request.files and request.form.get("name"):
            project_name    =   request.form.get("name")
            caption         =   request.form.get("caption")
            images          =   request.files.getlist("image")

            if(Projects.objects(project_name = project_name)):
                projectCounter = Projects.objects.all().count()
                return render_template("user.html", gallery = imgGallery(), 
                projectCounter = projectCounter, rProjects = rProjects[0], imageList = rProjects[1], msg = "Project Name already Exists. Try different name", Alert_Flag = False)
            else:
                projects = Projects()
                projects.project_name       =   project_name
                projects.project_caption    =   caption
                
                #File Upload
                counter = 1
                for image in images:
                    filename = secure_filename(project_name + "_" + str(counter) + ".jpg")
                    
                    #Store image width and height
                    # save bytes in a buffer
                    image_bytes = BytesIO(image.stream.read())
                    #produces a PIL Image object
                    photo = Image.open(image_bytes)
                    #Store image width and height
                    w, h = photo.size
                    #make the image editable
                    drawing = ImageDraw.Draw(photo)
                    font = ImageFont.truetype("C:/Users/SRJ/SJInteriors/application/static/fonts/Roboto-Black.ttf", 27)
                    #get text width and height
                    text = "© SJ Life Spaces Interiors"
                    text_w, text_h = drawing.textsize(text, font)
                    #store the position
                    pos = int(w/2 - text_w/2), int(h/2 - text_h/2)
                    #giving text color
                    c_text = Image.new('RGB', (text_w, text_h), color = '#000000')
                    drawing = ImageDraw.Draw(c_text)
                    #Background color and setting font
                    drawing.text((0,0), text, fill="#ffffff", font = font) #Background color
                    c_text.putalpha(100)
                    #pasting watermark on image
                    photo.paste(c_text, pos, c_text)
                    #saving image
                    photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

                    path = app.config['UPLOAD_FOLDER'] + filename
                    image_path = path[path.find('static'):]
                    gallery =   Gallery()
                    gallery.image_name      =   filename
                    gallery.image_path      =   image_path 
                    gallery.project_name    =   project_name 
                    
                    counter = counter + 1
                    gallery.save()
                projects.save()
                projectCounter = Projects.objects.all().count()
                return render_template("user.html", gallery = imgGallery(), 
                projectCounter = projectCounter, rProjects = rProjects[0], imageList = rProjects[1], msg = "Uploaded Successfully!", Alert_Flag = True)


#User: Delete Project:
@app.route("/delete_project/<string:name>")
def delete_project(name):
    if not session.get('login'):
        return redirect(url_for('login'))
    if Projects.objects(project_name = name):
        project = Projects.objects(project_name = name)
        project.delete()
        gallery = Gallery.objects(project_name = name)
        for image in gallery:
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], image.image_name))
        gallery.delete()
        return redirect(url_for('users'))
    else:
        return redirect(url_for('users'))


#User: Delete Image:
@app.route("/delete_image/<string:name>")
def delete_image(name):
    if not session.get('login'):
        return redirect(url_for('login'))
    if Gallery.objects(image_name = name):
        image = Gallery.objects.get(image_name = name)
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], image.image_name))
        image.delete()
        return redirect(url_for('projects'))
    else:
        return redirect(url_for('projects'))


#Mail: Contact Us | Sending Mail to Client and Company:
@app.route("/contactus", methods = ['GET','POST'])
def contactus():
    if request.method == 'GET':
        return redirect(url_for('index'))
    else:
        name        =   request.form.get("name")
        mobile_no   =   request.form.get("mobile_no")
        email       =   request.form.get("email")
        message     =   request.form.get("message")
        msg_to_client = Message("SJInteriors Booking",
                    sender="sales.sjlifespacesinteriors@gmail.com",
                    recipients=[email])
        msg_to_client.html = ("Hi {name},<br><br>Welcome to <b>SJLifeSpace Interiors</b>!<br><br>"
        "We are happy to make your life space more beautiful through your Home interiors."
        " Our agent will reach out to you. Thanks for contacting us. ".format(name = name))
        mail.send(msg_to_client)

        msg_to_company = Message("New Booking | {name} | {mobile_no}".format(name = name, mobile_no = mobile_no),
                    sender="sales.sjlifespacesinteriors@gmail.com",
                    recipients=["sales.sjlifespacesinteriors@gmail.com"])
        msg_to_company.html = ("Hi Sir,<br><br>You got a new booking today!<br>"
        "<h3><u>Client Details:</u></h3>"
        "Name : {name}<br>Mobile No.: {mobile_no}<br>Email ID: {email}<br>Message from Client: <b>{message}</b><br><br>"
        "Please contact the client to keep in touch "
        "and confirm the contract. :-)<br>".format(name = name, mobile_no = mobile_no, email = email, message = message))
        mail.send(msg_to_company)

        return redirect(url_for('index'))


#Feedback:
@app.route("/feedback", methods = ['GET','POST'])
def feedback():
    if request.method == 'GET':
        return redirect(url_for('index'))
    else:
        name        =   request.form.get("name")
        email       =   request.form.get("mail")
        message    =   request.form.get("feedback_message")

        #Mail to Client
        msg_to_client = Message("SJInteriors Feedback Response",
                    sender="sales.sjlifespacesinteriors@gmail.com",
                    recipients=[email])
        #Mail to Client---Mail Content
        msg_to_client.html = ("Hi {name},<br><br>Thanks for your valuable feedback!<br><br>"
        "We are extremely grateful that you took the time to send us your feedback about our Service."
        "We will read through your feedback carefully, and consider your suggestions to be very insightful.<br><br>"
        "Thanks once again and looking forward to hearing more from you.".format(name = name))
        mail.send(msg_to_client)

        #Mail to Company
        msg_to_company = Message("Feedback | {name} ".format(name = name),
                    sender="sales.sjlifespacesinteriors@gmail.com",
                    recipients=["sales.sjlifespacesinteriors@gmail.com"])
        #Mail to Company---Mail Content
        msg_to_company.html = ("Hi Sir,<br><br>You got a new feedback!<br>"
        "<h3><u>Client Details:</u></h3>"
        "Name : {name}<br>Email ID: {email}<br><br><h2><u>Feedback from Client: </u></h2>"
        "<b>{message}</b><br><br>".format(name = name, email = email, message = message))
        mail.send(msg_to_company)

        return redirect(url_for('index'))

		
#Project Gallery:
@app.route("/gallery", methods = ['GET','POST'])
@app.route("/gallery/<string:name>", methods = ['GET','POST'])
def project_gallery(name = None):
    if request.method == 'POST':
        name = request.form.get("name")
        print("Project Name ::::::::", name)
        project = Projects.objects.get(project_name = name)
        print("Project Name ::::::::", project.project_caption)
        images = Gallery.objects(project_name = name)
        return render_template("project_Gallery.html", gallery = images, project = project, is_projectgallery = True)
    else:
        return redirect("project_Gallery.html") 


#Display Projects:
@app.route("/projects")
def projects():
    if not session.get('login'):
        return redirect(url_for('login'))
    projects    =   Projects.objects.all()
    return render_template("projects.html", projects = projects)


#Update Project: 
@app.route("/updateProject", methods = ['GET','POST'])
def updateProject():
    if not session.get('login'):
        return redirect(url_for('login'))

    if request.method == 'GET':
        return redirect(url_for('projects'))
    else:
        project_name    =   request.form.get("name")  
        if request.form.get("caption"):
            caption =   request.form.get("caption")
            project = Projects.objects(project_name = project_name).update(project_caption = caption)
            return redirect(url_for('projects'))
        if request.files.getlist("image"):
            images          =   request.files.getlist("image")
            #File Upload
            counter = (Gallery.objects(project_name = project_name).count()) + 1 
            for image in images:
                filename = secure_filename(project_name + "_" + str(counter) + ".jpg")
                
                #Store image width and height
                # save bytes in a buffer
                image_bytes = BytesIO(image.stream.read())
                #produces a PIL Image object
                photo = Image.open(image_bytes)
                #Store image width and height
                w, h = photo.size
                #make the image editable
                drawing = ImageDraw.Draw(photo)
                font = ImageFont.truetype("C:/Users/SRJ/SJInteriors/application/static/fonts/Roboto-Black.ttf", 27)
                #get text width and height
                text = "© SJ Life Spaces Interiors"
                text_w, text_h = drawing.textsize(text, font)
                #store the position
                pos = int(w/2 - text_w/2), int(h/2 - text_h/2)
                #giving text color
                c_text = Image.new('RGB', (text_w, text_h), color = '#000000')
                drawing = ImageDraw.Draw(c_text)
                #Background color and setting font
                drawing.text((0,0), text, fill="#ffffff", font = font) #Background color
                c_text.putalpha(100)
                #pasting watermark on image
                photo.paste(c_text, pos, c_text)
                #saving image
                photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

                path = app.config['UPLOAD_FOLDER'] + filename
                image_path = path[path.find('static'):]
                gallery =   Gallery()
                gallery.image_name      =   filename
                gallery.image_path      =   image_path 
                gallery.project_name    =   project_name 
                
                counter = counter + 1
                gallery.save()
        return redirect(url_for('users'))
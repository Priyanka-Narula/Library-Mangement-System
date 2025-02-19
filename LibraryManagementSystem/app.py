# creating application objects and run

from flask import Flask,render_template,request
from application.database import db

app = None  #creating app object and assign it to none

def create_app():  #creating the function to make the configurations better,so that every time the func runs evrything gets incorporated
   app =Flask(__name__) # creating a app object.__name__ refers to current module i.e app.py(it refers to)
   app.debug = True
   app.config['SQLALCHEMY_DATABASE_URI'] ="sqlite:///lms1data.sqlite3"
   db.init_app(app)
   app.app_context().push()  #adding app context.gives a context of application to server.to specify that thsi app.py should run as server code .this line is giving sense to line 6
   return app

app = create_app()

from application.controllers import *
if __name__=='__main__':
    app.debug = True
    db.create_all()
    app.run()


            

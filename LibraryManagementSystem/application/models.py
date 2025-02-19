from .database import db #since app.py is outside the application folder and models.py will need to use the db object created in database.py that lies in the same folder i.e appplication so we need to add .database means telling models .py to import db from the folder where you exist istead of the app.py(root folder) 

class User(db.Model):

    __tablename__="user"
    u_id=db.Column(db.Integer(),primary_key = True)
    username=db.Column(db.String(),nullable = False , unique = True)
    first_name=db.Column(db.String(),nullable= False)
    last_name=db.Column(db.String(),nullable= False)
    password=db.Column(db.String(),nullable = False)
    email=db.Column(db.String(),nullable = False)
    type=db.Column(db.String,default = "user",nullable=False)
    user_rel=db.relationship("Issue" , backref = "user") 
    #issued_details=db.relationship("Books",secondary="issue",backref="user")
    
    

class Books(db.Model) :
    b_id=db.Column(db.Integer(),primary_key = True)
    b_title=db.Column(db.String(),nullable= False)  
    b_date_created=db.Column(db.String(),nullable=False)  
    b_author=db.Column(db.String(),nullable= False)
    b_cover_img=db.Column(db.String())
    b_url=db.Column(db.String(),nullable= False)
    #b_genre=db.Column(db.string(),nullable= False)
    b_description=db.Column(db.String(),nullable= False)
    g_id=db.Column(db.Integer(),db.ForeignKey("genre.id")) #here genre is table name in database and class name is Genre
     
class Genre(db.Model) :  
    __tablename__="genre"
    id=db.Column(db.Integer(),primary_key = True)
    g_name=db.Column(db.String(),nullable= False)
    #date_created=db.Column(db.string(),nullable=False)
    genre_filter=db.relationship("Books" , backref = "genre" ,cascade='all, delete-orphan') #using this we will retrieve all the books in particular genre

class Issue(db.Model):

    __tablename__="issue"
    id=db.Column(db.Integer(),primary_key = True)
    internal_status=db.Column(db.String(),nullable= False, default="requested")   #can be requested /approved /returned/rejected
    b_id=db.Column(db.Integer(),db.ForeignKey("books.b_id"))
    u_id=db.Column(db.Integer(),db.ForeignKey("user.u_id"))
    i_b_name=db.Column(db.String())
    is_date=db.Column(db.Date)
    ret_date=db.Column(db.Date)
    
class Request(db.Model):

    __tablename__="request"
    id=db.Column(db.Integer(),primary_key = True)
    b_id=db.Column(db.Integer(),db.ForeignKey("books.b_id"))
    u_id=db.Column(db.Integer(),db.ForeignKey("user.u_id"))
    r_b_name=db.Column(db.String())
    req_date=db.Column(db.Date)
    r_ret_date=db.Column(db.Date)



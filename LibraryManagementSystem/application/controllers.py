from flask import Flask,render_template,redirect,request,url_for,session,flash
from flask import current_app as app #flask will understand current app refering to app.py((where the app is created ) to avoid circular import among the files
from .models import * #for importing models to controllers and then controllers are imported in app.py ,so models will be available in app .py
from datetime import date,datetime

app.secret_key = 'hellowhatsgoingon123456'

#app is used in this module so we create another object with same alias as app 
#base url http://127.0.0.1:5000

@app.route('/')
def homepage():
    return render_template('homepage.html')

@app.route('/signin', methods= ['GET' , 'POST'])
def user_signin():
    if request.method == "POST" :
        u_name = request.form.get("u_name")
        pwd = request.form.get("pwd")
        this_user=User.query.filter_by(username = u_name).first() 
        if this_user:
            if this_user.password == pwd:
                if this_user.type == "admin":
                    return redirect('/admin')
                else:
                    session['user_id'] = this_user.u_id  # session.get('user_id') or session['user_id']
                    #return redirect(f'/user/{this_user.u_id}')
                    return redirect(f'/user')
                return render_template("user_dash.html", u_name = u_name)
            else:
                return "Incorrect Password"
        else:
            return "User doesn't exist"    
     
    return render_template('signin.html')

@app.route('/register', methods= ['GET' , 'POST'])
def user_register():
    if request.method == "POST" :
        u_name = request.form.get("u_name")
        f_name = request.form.get("f_name")
        l_name = request.form.get("l_name")
        pwd = request.form.get("pwd")
        email=request.form.get("email")
        #type = request.form.get("type")
        #this_user=User.query.filter_by(username = u_name).first() 
        if User.query.filter_by(username = u_name).first() :
            #if this_user:
            return "user already exists!"
        else:
            new_user=User(username=u_name , first_name = f_name ,last_name = l_name ,password = pwd ,email = email )
            db.session.add(new_user)
            db.session.commit()
            return redirect('/signin')
        
    return render_template('register.html')


@app.route('/admin', methods = ['GET', 'POST'])
def admin_signin():
    
    admin=User.query.filter_by(type = "admin").first()
    #return render_template("admin_dash.html")
    return redirect(url_for("admin_dash"))

#@app.route('/user/<int:user_id>', methods = ['GET', 'POST'])
@app.route('/user', methods = ['GET', 'POST'])
def user():
    #user=User.query.get(user_id)
    uid=session['user_id']
    user=User.query.get(uid)
    #issue_history=user.issued_details
    return render_template('user_dash.html', u_name = user.username,books=Books.query.all(),recent_books=Books.query.order_by(Books.b_id.desc()).limit(5).all())
    #return render_template('user_dash.html', u_name = user.username , issue_history = issue_history)


@app.route('/issue_book' , methods = ['GET', 'POST'])
def issue_book():

    if request.method == "POST":
        user_id = session['user_id']
        current_request_count =Issue.query.filter(Issue.u_id == user_id).count()
        current_approved_count=Request.query.filter(Request.u_id == user_id).count()
        total_count=current_request_count+current_approved_count
        if total_count >= 5:
            flash('You have reached the maximum limit of 5 book requests.')
            return redirect(url_for('user'))
        else:
            u_name=request.form.get("u_name")
            issue_date=request.form.get("issue_date")
            i_book_id=request.form.get("i_book_id")
            userid=session['user_id']
            i_book_name=Books.query.filter(Books.b_id == i_book_id).first()
            bname=i_book_name.__dict__.get('b_title')
            cur_date = date.today()
            retn_date = datetime.strptime(issue_date, '%Y-%m-%d').date()
            issue = Issue(b_id=i_book_id, u_id =userid ,i_b_name=bname, is_date= cur_date ,ret_date=retn_date )
            db.session.add(issue)
            db.session.commit()
            flash("Book sucessfully requested")
            return redirect(url_for("user"))
    return redirect(url_for("user"))




@app.route('/search' , methods = ['GET' , 'POST'])
def search():

    if request.method == 'POST':
        value=request.form['searchInput']
        searchType = request.form['searchType']
        value = value.title()

        if searchType == 'option1':
            searchResult = Books.query.filter(Books.b_title.like('%'+ value +'%')).all()
        elif searchType == 'option2':
            searchResult = Books.query.filter(Books.b_author.like('%'+ value +'%')).all()
            
        elif searchType == 'option3':
            gen = Genre.query.filter(Genre.g_name.like('%'+ value +'%')).first()
            s_g_id = gen.id
            searchResult = Books.query.filter(Books.g_id == s_g_id).all()   
            
        return render_template('searchresult.html' , searchResult = searchResult )
    return redirect(url_for('search'))


@app.route('/profile' ,methods  = ['POST', 'GET'])  # this is route for my books
def profile():

    u_id=session['user_id']
    user=User.query.get(u_id) #this is u_id from d/b created in line 122
    issue=Issue.query.filter(Issue.u_id == u_id).all()
    request=Request.query.filter(Request.u_id == u_id).all()
    return render_template('user_profile.html', userinfo=user ,issueinfo=issue , requestinfo = request  )


@app.route('/returnbook/<int:request_id>' ,methods  = ['POST', 'GET'])
def returnbook(request_id):
    r_book=Request.query.get(request_id)
    db.session.delete(r_book)
    db.session.commit()
    return redirect(url_for('profile'))


@app.route('/userdetails' ,methods  = ['POST', 'GET'])
def userdetails():

    u_id=session['user_id']
    user=User.query.get(u_id) #this is u_id from d/b created in line 122
    return render_template('userdetails.html', userinfo=user )


@app.route('/cancelreq/<int:issue_id>' ,methods  = ['POST', 'GET'])
def cancelreq(issue_id):
    cancel_req=Issue.query.get(issue_id)
    db.session.delete(cancel_req)
    db.session.commit()
    return redirect(url_for('profile'))


@app.route('/admin_dash' ,methods  = ['POST', 'GET'])
def admin_dash():
    issue_req=Issue.query.all()
    total_books=Books.query.count()
    total_genre=Genre.query.count()
    total_request=Request.query.count()
    # for issue in issue_req:
    #     issue_b_id=issue.b_id
    #     output=Books.query.filter(Books.b_id == issue_b_id).with_entities(Books.b_title).first()
    #     result=output[0]
    approved=Request.query.all()
    return render_template('admin_dash.html' ,prequest = issue_req ,app_req = approved ,total_books = total_books ,total_genre =total_genre ,total_request =total_request)



@app.route('/admincancelreq/<int:issue_id>' ,methods  = ['POST', 'GET'])
def admincancelreq(issue_id):
    cancel_req=Issue.query.get(issue_id)
    db.session.delete(cancel_req)
    db.session.commit()
    return redirect(url_for('admin_dash'))


@app.route('/approveissue_req/<int:issue_id>' ,methods  = ['POST', 'GET'])
def approveissue_req(issue_id):
    app_req=Issue.query.get(issue_id)
    
    add_to_request=Request(b_id = app_req.b_id ,
                            u_id = app_req.u_id ,
                            r_b_name= app_req.i_b_name,
                            req_date = app_req.is_date ,
                              r_ret_date = app_req.ret_date)
    db.session.add(add_to_request)
    db.session.delete(app_req)
    db.session.commit()
    return redirect(url_for('admin_dash'))


@app.route('/revoke/<int:request_id>' ,methods  = ['POST', 'GET'])
def revoke(request_id):
    revoke_req=Request.query.get(request_id)
    db.session.delete(revoke_req)
    db.session.commit()
    return redirect(url_for('admin_dash'))


@app.route('/backuser')
def backuser():
    return redirect(url_for("user"))


@app.route('/logout')
def logout():
    session.pop('user_id',None)
    return render_template('homepage.html')


@app.route('/admin_manage' ,methods  = ['POST', 'GET'])
def admin_manage():    
    
    return render_template('admin_manage.html' )


@app.route('/logoutadmin')
def logoutadmin():
    
    return render_template('homepage.html')


@app.route('/backadmin')
def backadmin():
    
    return redirect(url_for("admin_dash"))


@app.route('/add_genre' ,methods  = ['POST', 'GET'])
def add_genre():
    
    if request.method == "POST" :
        g_name=request.form.get('g_name')
        new_genre=Genre(g_name = g_name)
        db.session.add(new_genre)
        db.session.commit()
        return render_template("admin_manage.html")
        
    else:
        return render_template("add_genre.html")
    
    
    
@app.route('/update_genre',methods  = ['POST', 'GET'])
def update_genre():    
        genreinfo=Genre.query.all()
        
        return render_template("update_genre.html",genre = genreinfo)



@app.route('/deletegenre/<int:genre_id>' ,methods  = ['POST', 'GET'])
def deletegenre(genre_id):
    genre_del=Genre.query.get(genre_id)
    book_del=Books.query.filter_by(g_id = genre_id)
    for book in book_del:
        db.session.delete(book)
        db.session.commit()
    db.session.delete(genre_del)
    db.session.commit()
    return redirect(url_for('update_genre'))
    


@app.route('/edit_genre/<int:genre_id>' ,methods  = ['POST', 'GET'])
def edit_genre(genre_id):
    if request.method == "POST" :
        genre_edit=Genre.query.get(genre_id)
        n_g_name=request.form.get('g_name')
        genre_edit.g_name=n_g_name
        db.session.commit()
        return redirect(url_for("update_genre"))
    else:
        return render_template("edit_genre.html")



@app.route('/add_book' ,methods  = ['POST', 'GET'])
def add_book():
    
    if request.method == "POST" :
        b_title=request.form.get('b_title')
        b_year=request.form.get('b_year')
        b_author=request.form.get('b_author')
        b_img=request.form.get('b_img')
        b_url=request.form.get('b_url')
        b_descp=request.form.get('b_descp')
        b_g_id=request.form.get('b_g_id')
        
        new_book=Books(b_title = b_title , b_date_created = b_year ,b_author = b_author , b_cover_img = b_img ,
                       b_url = b_url,
                       b_description = b_descp,
                       g_id = b_g_id)
        print(new_book)
        db.session.add(new_book)
        db.session.commit()
        return render_template("admin_manage.html")
    else:
        return render_template("add_book.html")
    

    
@app.route('/allbooks',methods  = ['POST', 'GET']) #route to show all books to admin to delete and update
def allbooks():  
        bookinfo=Books.query.all()  
        if request.method == 'POST':
            book_id=request.form.get('book_id')
            book_title=request.form.get('book_title')
            book_year=request.form.get('book_year')
            book_author=request.form.get('book_author')
            book_image=request.form.get('book_image')
            book_url=request.form.get('book_url')
            book_descp=request.form.get('book_descp')
            book_genre=request.form.get('book_genre')
            book_edit=Books.query.get(book_id)
            book_edit.b_title=book_title
            book_edit.b_date_created=book_year
            book_edit.b_author=book_author
            book_edit.b_cover_img=book_image
            book_edit.b_url=book_url
            book_edit.b_description=book_descp
            book_edit.g_id=book_genre
            db.session.commit()
            return redirect(url_for("allbooks")) 
        else:
            return render_template("allbooks.html",allbooks = bookinfo) 
        
        
    
@app.route('/deletebook/<int:book_id>',methods  = ['POST', 'GET'])
def deletebook(book_id):  
               
        book_del=Books.query.get(book_id)
        db.session.delete(book_del)
        db.session.commit()
        return redirect(url_for("allbooks"))
         
    

@app.route('/read/<int:book_id>' ,methods  = ['POST', 'GET'])
def read(book_id):
    book=Books.query.filter_by(b_id = book_id).first()
    print(book)
    book_n= book.b_title
    print(book_n)
    book_d=book.b_description

    return render_template("readbook.html" , book_name = book_n ,book_content = book_d)

















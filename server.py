import psycopg2
import psycopg2.extras
import os
import sys
reload(sys)
import uuid
import time
import string
import cgitb, cgi
from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO, emit, send, join_room, leave_room
sys.setdefaultencoding("UTF8")


from subprocess import call
call(["sudo","service","postgresql","start"])

app = Flask(__name__, static_url_path='')
app.config['SECRET_KEY'] = 'secret!'
app.secret_key = os.urandom(24).encode('hex')

socketio = SocketIO(app)

page = ""

@app.route('/')
def mainIndex():


  return render_template('index.html')

  
#######################################Finishedish stuff ################################
def connectToDB():
    connectionString = 'dbname=bikesdb user=postgres password=1234 host=localhost'
    print (connectionString)
    try:
      return psycopg2.connect(connectionString)
    except:
      print("Can't connect to database")
   
   
  
@app.route('/search', methods=['GET','POST'])
def search():
    results = [];
    conn = connectToDB()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
   
    searchTerm = '%' + request.form['Search'] + '%'
    
    print searchTerm
    
    cmd = cur.execute("select author from blogs where author like %s", (searchTerm,))
    try:
      cur.execute("select author from blogs where author like %s", (searchTerm,))
      results = cur.fetchall()
      print results
      
    except:
      print("Error executing select")
      print cmd
      
    
    return render_template('search.html', results=results)


@app.route('/news', methods=['GET'])
def news():
  
  return render_template('news.html')
  
  
  
@app.route('/blog', methods=['GET'])
def blog():
    results = [];
    conn = connectToDB()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cmd = """select * from blogs;"""
    try:
      cur.execute(cmd)
      results = cur.fetchall()
      print results
      
    except:
      print("Error executing select category")
      print cmd
    return render_template('blog.html', blogs=results)
    


@app.route('/contact', methods=['GET'])
def contact():
  
  return render_template('contact.html')
  
  
@app.route('/shop', methods=['GET'])
def shop():
  
  return render_template('shop.html')  
  

@app.route('/layout', methods=['GET', 'POST'])
def sesh():
  conn = connectToDB()
  cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
  if 'UserEmail' in session:
    print ("true")
  else:
    return redirect(url_for('mainIndex'))
 
  user=[session['UserEmail'],session['UserFirstName'], session['UserLastName']]

  print(user[0])
  
  return render_template('layout.html')

  
@app.route('/signup', methods=['GET','POST'])
def signup():
  conn = connectToDB()
  cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
  print("getting into socket")
  
  if request.method == 'POST':
    email = request.form['email']
    firstName = request.form['firstName']
    lastName = request.form['lastName']
    password = request.form['password']
    confirmpassword = request.form['confirmpassword']
  
    if password == confirmpassword:
      cur.execute("select * from users WHERE email = %s", (email,))
      if cur.fetchone():
        print("Account already registered to that name.")
        print('registerfailure', "Email already registered!")
      
      else:
        cur.execute("INSERT INTO users (email, firstName, lastName, password) VALUES (%s, %s, %s, crypt(%s, gen_salt('bf')));", (email, firstName, lastName, password))
        conn.commit()
      
    else:
      print('registerfailure', "Passwords don't match!")
      
    return redirect(url_for('registered'))
  
  
  return render_template('signup.html')
  

@app.route('/registered', methods=['GET'])
def registered():
  
  return render_template('registered.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
  conn = connectToDB()
  cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
  print("Makes it to login")
  if request.method == 'POST':
    username = request.form['email']
    password = request.form['password']
    
    cur.execute("select * from users where email = %s and password = crypt(%s, password);", (username, password))
    row = cur.fetchone()
    while row is not None:
      session['UserFirstName'] = row['firstname']
      session['UserLastName'] = row['lastname']
      session['UserEmail'] = row['email']
      print(session['UserFirstName'])
      return redirect(url_for('sesh'))
    else:
      return redirect(url_for('mainIndex'))
  else:
    return redirect(url_for('mainIndex'))

  
@app.route('/product', methods=['GET'])
def product():
  """rows returned from postgres are a python dictionary (can
  also be treated as an ordered list)"""
  conn = connectToDB()
  cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
  try:
    cur.execute("select * from items where name = 'Seat';")
  except:
    print("Error executing select one product")
  results = cur.fetchall()
  print results
  #for r in results:
    #print r['artist']
  return render_template('product.html', items=results)
  
@app.route('/addProduct', methods=['GET', 'POST'])
def addTo():
    results = []
    conn = connectToDB()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == 'POST':
        form = cgi.FieldStorage()
        
        if request.form['submit'] == 'Search':
                try:
                  cmd = """SELECT * FROM items WHERE name = '%s';""" % (request.form['name'])
                  print(cmd)
                  cur.execute(cmd)
                  results = cur.fetchall()
                  
                  return render_template('addProduct.html', item = results[0])
                except:
                  print("Could not find %s" % request.form['name'] )
                  
        elif request.form['submit'] == 'Modify Product':
                try:
                  cmd = """UPDATE items SET name = '%s', description = '%s', category = '%s', retailPrice = '%s', salesprice = '%s', specifications = '%s', reviews = '%s', manufacturer = '%s', stock = '%s', stocklimit = '%s', image = '%s' WHERE name = '%s';""" % (fixApost(request.form['name'].encode('utf-8')), fixApost(request.form['description'].encode('utf-8')), fixApost(request.form['category'].encode('utf-8')), request.form['retailPrice'].encode('utf-8'), request.form['salesPrice'].encode('utf-8'), fixApost(request.form['specifications'].encode('utf-8')),  fixApost(request.form['reviews'].encode('utf-8')), fixApost(request.form['manufacturer'].encode('utf-8')), request.form['stock'].encode('utf-8'),  request.form['stockLimit'].encode('utf-8'), request.form['imageName'].encode('utf-8'), fixApost(request.form['name'].encode('utf-8')))
                  print(cmd) 
                  cur.execute(cmd)
                except:
                  print("Could not update %s" % (fixApost(request.form['name'].encode('utf-8'))))
                  conn.rollback()
        
                conn.commit()  
        elif request.form['submit'] == 'Add Product':
            # add new entry into database
                try:
                    cmd = """INSERT INTO items (name, description, category, retailPrice, salesPrice, specifications, reviews,  manufacturer, stock, rating, stockLimit, image) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '5', '%s');""" % (fixApost(request.form['name'].encode('utf-8')), fixApost(request.form['description'].encode('utf-8')), fixApost(request.form['category'].encode('utf-8')), request.form['retailPrice'].encode('utf-8'), request.form['salesPrice'].encode('utf-8'), fixApost(request.form['specifications'].encode('utf-8')),  fixApost(request.form['reviews'].encode('utf-8')), fixApost(request.form['manufacturer'].encode('utf-8')), request.form['stock'].encode('utf-8'),  request.form['stockLimit'].encode('utf-8'), request.form['imageName'].encode('utf-8'))
                   
                    
                    #print(cmd)
                    cur.execute(cmd)    
                except:
                    print("ERROR inserting into items")
                    print("INSERT INTO items (name, description, category, retailPrice, salesPrice, specifications, reviews,  manufacturer, stock, rating, stockLimit) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '5');" % (fixApost(request.form['name'].encode('utf-8')), fixApost(request.form['description'].encode('utf-8')), fixApost(request.form['category'].encode('utf-8')), request.form['retailPrice'].encode('utf-8'), request.form['salesPrice'].encode('utf-8'), fixApost(request.form['specifications'].encode('utf-8')),  fixApost(request.form['reviews'].encode('utf-8')), fixApost(request.form['manufacturer'].encode('utf-8')), request.form['stock'].encode('utf-8'),  request.form['stockLimit'].encode('utf-8')))
                    
        
                    conn.rollback()
        
                conn.commit()
    return render_template('addProduct.html', item=results)


def fixApost(inString):
    if "'" in inString:
        inString = string.replace(inString, "'", "''")
    return inString       
  


@app.route('/cart', methods=['GET','POST'])
def cart():
  
  if request.method == 'POST':
    return redirect(url_for('checkout'))
  
  return render_template('cart.html')
  
  
@app.route('/checkout', methods=['GET','POST'])
def checkout():
  
  return render_template('checkout.html')

  
@app.route('/category/<inCategory>/', methods=['GET'])
def category(inCategory):
    results = [];
    print url_for('signup')
    conn = connectToDB()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    print inCategory;
    if(inCategory == "all"):
      cmd = """select * from items;"""
    else:
      cmd = """select * from items where category = '%s';""" % (inCategory)
      
    try:
      cur.execute(cmd)
      results = cur.fetchall()
      print results
      
    except:
      print("Error executing select category")
      print cmd
    return render_template('category.html', items=results, cat = inCategory)

# start the server
if __name__ == '__main__':
    #app.run(host='0.0.0.0', debug=True, port=12345, use_reloader=True)
    app.run(host=os.getenv('IP', '0.0.0.0'), port =int(os.getenv('PORT', 8080)), debug=True)

import psycopg2
import psycopg2.extras
import os
import sys
import uuid
import time
from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO, emit, send, join_room, leave_room

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

    
@socketio.on('register', namespace='/bikeShop')
def register(email, pw, cpw, fn, ln):
  conn = connectToDB()
  cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
  print("getting into socket")
  if pw == cpw:
    cur.execute("select * from users WHERE email = %s", (email,))
    if cur.fetchone():
      print "Account already registered to that name"
      emit('registerfailure', "Email already registered!")
      
    else:
      cur.execute("INSERT INTO users (email, password, firstname, lastname) VALUES(%s, crypt(%s, gen_salt('bf')), %s, %s);", (email, pw, fn, ln))
      conn.commit()
      
  else:
    emit('registerfailure', "Passwords don't match!")
  
  
#######################################Finishedish stuff ################################
def connectToDB():
#  connectionString = 'dbname=music user=postgres password=PeekoT55! host=localhost'
    connectionString = 'dbname=bikesdb user=postgres password=1234 host=localhost'
    print (connectionString)
    try:
      return psycopg2.connect(connectionString)
    except:
      print("Can't connect to database")
      
   
   
@app.route('/news', methods=['GET'])
def news():
  
  return render_template('news.html')
  
  
  
@app.route('/blog', methods=['GET'])
def blog():
  
  return render_template('blog.html')
  
  

@app.route('/contact', methods=['GET'])
def contact():
  
  return render_template('contact.html')
  
  
@app.route('/shop', methods=['GET'])
def shop():
  
  return render_template('shop.html')  
  
  
@app.route('/signup', methods=['GET','POST'])
def signup():
  
  return render_template('signup.html')
  
  
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
  
@app.route('/category/<inCategory>', methods=['GET'])
def category(inCategory):
    
    conn = connectToDB()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    print inCategory;
    try:
      cur.execute("""select (name, description, retailprice, salesprice) from items where category = 'parts';""")
      results = cur.fetchall()

      
    except:
      print("Error executing select category")
    return render_template('category.html', items=results)

# start the server
if __name__ == '__main__':
    #app.run(host='0.0.0.0', debug=True, port=12345, use_reloader=True)
    app.run(host=os.getenv('IP', '0.0.0.0'), port =int(os.getenv('PORT', 8080)), debug=True)

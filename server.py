import psycopg2
import psycopg2.extras
import os
from flask import Flask, render_template, request
app = Flask(__name__)

planes = ['Easy Flyer', 'UMX Radian']


@app.route('/music')
def showChart():
  """rows returned from postgres are just an ordered list"""
  
  conn = connectToDB()
  cur = conn.cursor()
  try:
    cur.execute("select artist, name from albums")
  except:
    print("Error executing select")
  results = cur.fetchall()
  return render_template('music.html', albums=results)

@app.route('/music3', methods=['GET', 'POST'])
def showChartForms():
  """rows returned from postgres are a python dictionary (can
  also be treated as an ordered list)"""
  conn = connectToDB()
  cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
  if request.method == 'POST':
    # add new entry into database
    try:
      cur.execute("""INSERT INTO albums (artist, name, rank, released) 
       VALUES (%s, %s, %s, %s);""",
       (request.form['artist'], request.form['album'], request.form['rank'], request.form['released']) )
    except:
      print("ERROR inserting into albums")
      print("Tried: INSERT INTO albums (artist, name, rank, released) VALUES ('%s', '%s', %s, %s);" %
        (request.form['artist'], request.form['album'], request.form['rank'], request.form['released']) )
      conn.rollback()
    conn.commit()

  try:
    cur.execute("select artist, name, rank, released from albums")
  except:
    print("Error executing select")
  results = cur.fetchall()
  print results
  for r in results:
    print r['artist']
  return render_template('music3.html', albums=results)

    
p2 = [{'person': 'Samantha Young', 'model': 'Pizza', 'time': '7pm', 'bday': '1990-07-20'},
{'person': 'Elizabeth Simmons', 'model': 'Hamburger', 'time': '6pm', 'bday': '1985-06-19'},
{'person': 'Glenn Taylor', 'model': 'Nachos', 'time': '7pm', 'bday': '1995-03-01'}]

@app.route('/r2', methods=['GET', 'POST'])
def regs():
    if request.method == 'POST':
        p2.append({'person': request.form['name'],
                   'model': request.form['plane'],
                   'time' : request.form['time'],
                   'bday' : request.form['bday']})
    return render_template('r2.html', selected='r2', planes=p2)
                   
@app.route('/')
def mainIndex():
    
    theSpotlight = "Shrimp Pasta"
    isClass = True 
    project = {'date': '14 February', 'time': '3pm', 'dish': 'Fish Tacos', 'cost': '$20'}
    
    videos =[{'title': 'Giadas Chicken Cacciatore Recipe', 'vidLink': 'tQlSchHlo48', 'description': 'Giada makes chicken cacciatore, a rustic poultry-vegetable hunters stew'},
             {'title': 'Ultimate Super Bowl Sandwich', 'vidLink': '8unDwSlAJlQ', 'description': 'Epic Meal Time builds a Nacho Chicken Sandwich for Super Bowl'},
             {'title': 'Chocolate Pizza', 'vidLink': 'rmeGntwt-c8', 'description': 'Food Network TV Dinner Ideas'},
             {'title': 'Food Networks Chopped Kids', 'vidLink': 'pdUYl54CPSA', 'description': 'Chopped Kids Edition'}]
             
    return render_template('index.html', spotlight=theSpotlight, project=project, classC=isClass, posts=videos)

@app.route('/breakfest')
def breakfest():
    return render_template('breakfest.html')

@app.route('/lunch')
def lunch():
    return render_template('lunch.html')
    
@app.route('/dinner')
def dinner():
    return render_template('dinner.html')
    
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        planes.append(request.form['rcplane'])
    return render_template('register.html', selected='register', planes=planes)
   
@app.route('/registration2', methods=['POST'])
def reply():
    theplane=request.form['rcplane']
    return render_template('registration2.html', plane=theplane)
  
  
#######################################Finishedish stuff ################################
def connectToDB():
#  connectionString = 'dbname=music user=postgres password=PeekoT55! host=localhost'
    connectionString = 'dbname=gustybikeshopdb user=gustyAdmin password=1234 host=localhost'
    print (connectionString)
    try:
      return psycopg2.connect(connectionString)
    except:
      print("Can't connect to database")
      
      
@app.route('/showProduct', methods=['GET'])
def showPoduct():
  """rows returned from postgres are a python dictionary (can
  also be treated as an ordered list)"""
  conn = connectToDB()
  cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
  try:
    cur.execute("select artist, name, rank, released from albums")
  except:
    print("Error executing select")
  results = cur.fetchall()
  print results
  for r in results:
    print r['artist']
  return render_template('music3.html', albums=results)
    
# start the server
if __name__ == '__main__':
    #app.run(host='0.0.0.0', debug=True, port=12345, use_reloader=True)
    app.run(host=os.getenv('IP', '0.0.0.0'), port =int(os.getenv('PORT', 8080)), debug=True)

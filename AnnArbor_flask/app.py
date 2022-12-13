from flask import Flask
from flask import render_template
import sqlite3

app = Flask(__name__)

# Edit Configurations -> FLASK_DEBUG √



@app.route('/')
def index():
    return render_template('index.html')



@app.route('/index')
def home():
    # return render_template('index.html')
    return index()



@app.route('/post')
def title():
    datalist = []
    con = sqlite3.connect('annarbor_renting.db')  
    cur = con.cursor()                          
    sql = "select * from renting"               
    data = cur.execute(sql)
    for item in data:
        datalist.append(item)
    cur.close()                                 
    con.close()                                 
    return render_template('post.html', renting=datalist)  



@app.route('/picture')
def person():
    datalist = []
    con = sqlite3.connect('annarbor_renting.db')  
    cur = con.cursor()                          
    sql = "select * from renting"               
    data = cur.execute(sql)
    for item in data:
        datalist.append(item)
    cur.close()                                 
    con.close()  
    return render_template('picture.html', renting=datalist)


# 词云
@app.route('/word')
def count():
    return render_template('word.html')



@app.route('/info')
def info():
    datalist = []
    con = sqlite3.connect('annarbor_renting.db')  
    cur = con.cursor()                          
    sql = "select * from renting"               
    data = cur.execute(sql)
    for item in data:
        datalist.append(item)
    cur.close()                                 
    con.close()
    return render_template('info.html',renting = datalist)


if __name__ == '__main__':
    app.run()

from flask import Flask, render_template, request,redirect,url_for
import requests
import sqlite3 as sql


app = Flask(__name__)



list1 = [] 
@app.route('/')
def home():
    

    return render_template('home.html')

@app.route('/', methods =['POST', 'GET'])
def index():

    if request.form.get('chabtn', None) == "查询":
         trow = ""
         cityming =""
         citycloud = ""
         Tcitytem = ""
         citytime =""
         
         
         chabtn = ""
         con = sql.connect("weather.db")
         cur = con.cursor()
          
         city = request.form['text']
         timenow = (time_today,)
         cur.execute("select city from chaxun")
         citylist =  cur.fetchall()
         print(citylist)
         i = (city,)
         
         
         try:
              if i in citylist:
                   a = ""
                   b = ""
                   x = ""
                   y = ""


                   t = (city,)
                   con = sql.connect("weather.db")
                   cur = con.cursor()
                   cur.execute("select * from chaxun where city=? and ctime=date('now')",t)
                   trow = cur.fetchone()
                   con.commit()
                   x = trow[0]
                   y = trow[1]
                   a = trow[2]
                   b = trow[3]
                   list1.append('%s,%s,%s,%s' % (trow[0], trow[1], trow[2], trow[3]))
                   
                   return render_template('home.html',x=x,y=y,a=a,b=b)
              else: 
                                  
                   url = "https://api.seniverse.com/v3/weather/now.json?key=kelsy6uu0gufudjz&" + "location=%s&language=zh-Hans&unit=c" % city
                   r = requests.get(url)
                   dict2 = r.json()['results']
                   citycloud = dict2[0]['now']['text']
                   citytem = dict2[0]['now']['temperature'] 
                   cityming = dict2[0]['location']['name']
                   citytime = dict2[0]['last_update'].replace('T',' ')[:10]
    
                   Tcitytem = citytem +"℃"
                   
                   list1.append('%s,%s,%s,%s' % (cityming, citycloud, Tcitytem, citytime))
         
                   con = sql.connect("weather.db")
                   cur = con.cursor()
            
                   cur.execute("INSERT INTO chaxun (city,cloud,ctemp,ctime)\
                VALUES (?,?,?,?)",(cityming,citycloud,Tcitytem,citytime) )
              
                   con.commit()
                   return render_template('home.html',cityming=cityming,citycloud=citycloud, Tcitytem=Tcitytem ,citytime=citytime) 
         except KeyError:
              return render_template('newagain.html')
              
             
    elif  request.form.get('hisbtn', None) == "历史":
        return redirect(url_for('his'))
         
    elif  request.form.get('helpbtn', None) == "帮助":
        
         return redirect(url_for('h_elp'))   
         
    elif  request.form.get('gzbtn', None) == "更正":
         try:
         
              city = request.form['text']
              citygz,cloudgz = city.split(' ')
         
              with sql.connect("weather.db") as con: 
              
                   cur = con.cursor()
                 
                   cur.execute("UPDATE chaxun set cloud =?  where city =? ",(cloudgz,citygz))
                   con.commit()
                   rowl = "你更正了"+citygz + "的天气为" +cloudgz
                   return render_template("gz.html",rowl = rowl)
         except ValueError:
             
              return render_template("gesh.html")
   
     

  
      
    

@app.route('/h_elp', methods =['POST', 'GET'])
def h_elp():
    

    return render_template('help.html')

@app.route('/his', methods =['POST', 'GET'])
def his():

   return render_template("history.html",list1=list1)
   


if __name__ == '__main__':
    app.run(debug=True)
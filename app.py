from flask import Flask, request, render_template
import sqlite3

#connecting to the database and creating cursor
con = sqlite3.connect("database.db")
cr = con.cursor()

cr.execute("create table if not exists user(t_name TEXT, c_name TEXT, password TEXT, num TEXT, time TEXT, sub TEXT, Date TEXT, grade TEXT)")

#creating flask instance, name is the name of the current python module so flask knows where to look for templates
app = Flask(__name__)

#app route decorator specifies the function that should be called when the url passed as an argument is accessed
#rendering a template will replace the variable placeholders with inputted data  
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/View')
def View():
    return render_template('View.html')

@app.route('/schedule', methods=['POST', 'GET'])
def schedule():
    if request.method == 'POST':
        data = request.form #retrieves the data entered by the user as form data
        List = []
        for key in data:
            List.append(data[key]) #stores inputs into a list
        print(List)

        con = sqlite3.connect("database.db")
        cr = con.cursor()
        cr.execute("insert into user values(?,?,?,?,?,?,?,?)", List) #inserts inputs into database
        con.commit()

        return render_template('index.html', msg="Class scheduled successfully..")
    return render_template('index.html')

@app.route('/display', methods=['POST', 'GET'])
def display():
    if request.method == 'POST':
        Date = request.form['Date'] #getting the input date
        con = sqlite3.connect("database.db")
        cr = con.cursor()
        cr.execute("select * from user where date = '"+Date+"'")
        result = cr.fetchone() #connecting to databse and fetching the details for that day
        print(result)
        if result:
            return render_template('View.html', result=result) #rendering the data fetched from database
        else:
            return render_template('View.html', msg="There is no class scheduled on this date")
    return render_template('View.html')

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)

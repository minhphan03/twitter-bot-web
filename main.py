from flask import Flask,render_template, request
from tweetbot import webscraping
from flaskext.mysql import MySQL

app = Flask(__name__)
app.static_folder = 'static'

mysql = MySQL()
queue = []

#configuration
app.config['MYSQL_DATABASE_USER'] = 'MinhPhan'
app.config['MYSQL_DATABASE_PASSWORD']= 'MinhPhanIsComing'
app.config['MYSQL_DATABASE_DB'] = 'word'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

#homepage
@app.route("/")
def main():
    return render_template("form.html")

#redirection
@app.route("/form")
def main2():
    return render_template("form.html")

#after form submission
@app.route("/result", methods=['POST'])
def parse_content():
    _word = request.form['word']
    _def = webscraping(_word)
    return render_template("result.html", word=_word, definition=_def)

    #return json.dumps({'html':'<span>All fields good !!</span>'})

@app.route("/finish")
def finish_form():
    try:
        conn = mysql.connect()
        # cursor to query our stored procedures
        cursor = conn.cursor()
        global queue
        queue = []
        print(queue[0])
        print(queue[1])
        cursor.callproc('add_word',[queue[0],queue[1]])
        data = cursor.fetchall()
        queue = []
        #if the callproc has done work, no more data to process
        if len(data) == 0:
            conn.commit()
    except Exception as e:
        print(e)
    else:
        cursor.close()
        conn.close()

    return render_template("finish.html")

@app.route("/path", methods = ['GET','POST'])
def view():
    global queue
    queue[0] = request.form.get('word')
    queue[1] = request.form.get('def')
    return
if __name__ == "__main__":
    app.run()

from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from wordfinder import webscraping
from flaskext.mysql import MySQL
import json

app = Flask(__name__)

app.config["DEBUG"] = True
app.static_folder = 'static'

mysql = MySQL()
queue = {'Word': '', 'Def': ''}

# database configuration
app.config['MYSQL_DATABASE_USER'] = 'minhphan0612'
app.config['MYSQL_DATABASE_PASSWORD']= 'richardiscoming'
app.config['MYSQL_DATABASE_DB'] = 'minhphan0612$word'
app.config['MYSQL_DATABASE_HOST'] = 'minhphan0612.mysql.pythonanywhere-services.com'
mysql.init_app(app)

# SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
#     username="minhphan0612",
#     password="richardiscoming",
#     hostname="minhphan0612.mysql.pythonanywhere-services.com",
#     databasename="minhphan0612$word",
# )
# app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
# app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# db = SQLAlchemy(app)

# homepage
@app.route("/")
def main():
    return render_template("form.html")


# redirection
@app.route("/form")
def back():
    return render_template("form.html")


# after form submission
@app.route("/result", methods=['POST'])
def parse_content():
    _word = request.form['word']
    _def = webscraping(_word)
    return render_template("result.html", word=_word, definition=_def)


@app.route("/finish", methods = ['GET','POST'])
def finish_form():
    try:
        conn = mysql.connect()
        # cursor to query our stored procedures
        cursor = conn.cursor()

        global queue
        # clear memory
        queue['Word'] = ''
        queue['Def'] = ''

        queue['Word'] = request.form.get('w')
        queue['Def'] = request.form.get('d')

        if queue['Word'] != '' and queue['Def'] != '':
            cursor.callproc('add_word',[queue['Word'],queue['Def']])

        data = cursor.fetchall()
        # if the callproc has done work, no more data to process
        if len(data) == 0:
            conn.commit()

    except Exception as e:
        print(e)

    else:
        cursor.close()
        conn.close()

    finally:
        return render_template("finish.html")


if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, render_template, request, json
from wordfinder import webscraping
from flaskext.mysql import MySQL
import json

app = Flask(__name__)
app.static_folder = 'static'

mysql = MySQL()
queue = {'Word': '', 'Def': ''}

# database configuration
app.config['MYSQL_DATABASE_USER'] = 'MinhPhan'
app.config['MYSQL_DATABASE_PASSWORD']= 'MinhPhanIsComing'
app.config['MYSQL_DATABASE_DB'] = 'word'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)


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

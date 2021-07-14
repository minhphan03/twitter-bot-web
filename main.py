from flask import Flask,render_template, request, json

from tweetbot import webscraping

app = Flask(__name__)
app.static_folder = 'static'

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
    return render_template("result.html",word=_word,definition = _def)
    #return json.dumps({'html':'<span>All fields good !!</span>'})

@app.route("/finish")
def finish_form():
    return render_template("finish.html")

if __name__ == "__main__":
    app.run()

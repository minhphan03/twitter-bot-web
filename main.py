from flask import Flask,render_template, request, json

app = Flask(__name__)
app.static_folder = 'static'

#homepage
@app.route("/")
def main():
    return render_template("form.html")

#after form submission
@app.route("/result", methods=['POST'])
def parse_content():
    _word = request.form['word']
    _def = request.form['definition']
    return "<h1>hello</h1>"

if __name__ == "__main__":
    app.run()

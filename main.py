from flask import Flask,render_template

app = Flask(__name__)
app.static_folder = 'static'

#homepage
@app.route("/")
def main():
    return render_template("form.html")



if __name__ == "__main__":
    app.run()

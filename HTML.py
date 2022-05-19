import main
from flask import Flask
from flask import (render_template, request)


app = Flask(__name__)


@app.route('/result')
def result():
    urlname = request.args['name']
    result = main.getResult(urlname)
    return result

@app.route('/', methods=['GET', 'POST'])
def hello():
    return render_template("getInput.html")


if __name__ == '__main__':
    app.run(debug=True)

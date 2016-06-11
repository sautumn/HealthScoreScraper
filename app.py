from flask import Flask
from flask import Flask, render_template
import addtodb
import scrapermain

app = Flask(__name__)

@app.route("/")
def main():
    return render_template('index.html')

@app.route('/json')
def json_stuff():
	return addtodb.json_formatter()

if __name__ == "__main__":
    app.run()

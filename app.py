from flask import Flask
app = Flask(__name__)


from flask import render_template
@app.route('/')
def hello(name=None):
    return render_template('fanfix.html', name=name)

@app.route('/informationInput.html/')
def hello_world(name=None):
	return render_template('informationInput.html', name=name)

if __name__ == "__main__":
    app.run()

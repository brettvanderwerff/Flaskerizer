from flask import render_template
from Test_application import ap

@app.route('/index.html')
@app.route('/')
def index():
    return render_template('index.html')


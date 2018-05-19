from flask import Flask, render_template

app = Flask(__name__)

@app.route('/blog-grid.html')
def blog_grid():
    return render_template('blog-grid.html')

@app.route('/blog-single.html')
def blog_single():
    return render_template('blog-single.html')

@app.route('/index.html')
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
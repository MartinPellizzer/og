from flask import Flask, render_template
app = Flask (__name__)

posts = [
    {
        'author': 'Martin 1',
        'title': 'blog post 1',
        'content': 'content 1',
        'date_posted': 'april 21, 2018',
    },
    {
        'author': 'Martin 2',
        'title': 'blog post 2',
        'content': 'content 2',
        'date_posted': 'april 22, 2018',
    },
]

@app.route("/")
@app.route("/home")
def hello():
    return render_template('home.html', posts=posts)

@app.route("/about")
def about():
    return render_template('about.html', title='About')

if __name__ == '__main__':
    app.run(debug=True)
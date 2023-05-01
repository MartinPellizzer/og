from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm
app = Flask (__name__)

app.config['SECRET_KEY'] = 'd88ecef6c5e0f68a3d37202aa2aee45f'

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
def home():
    return render_template('home.html', posts=posts)


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)
    

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == '123':
            flash('You have been logged in', 'success')
            return redirect(url_for('home'))
        else:
            flash('login unsuccessful, check username and password', 'danger')

    return render_template('login.html', title='Login', form=form)



if __name__ == '__main__':
    app.run(debug=True)
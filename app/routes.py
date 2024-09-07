from flask import render_template, request, redirect, url_for, flash
from app import app, db
from app.models import BlogPost
from config import Config

@app.route('/')
@app.route('/page/<int:page>')
def index(page=1):
    posts = BlogPost.query.order_by(BlogPost.date_posted.desc()).paginate(
        page=page, 
        per_page=Config.POSTS_PER_PAGE,
        error_out=False
    )
    return render_template('index.html', posts=posts)

@app.route('/post/<int:post_id>')
def post(post_id):
    post = BlogPost.query.get_or_404(post_id)
    return render_template('blog_post.html', post=post)

@app.route('/categories')
def categories():
    categories = ['Python Basics', 'Web Development', 'Data Science', 'Machine Learning', 'Automation']
    return render_template('categories.html', categories=categories)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        # Here you can process the form data (e.g., send an email)
        flash('Your message has been sent successfully!', 'success')
        return redirect(url_for('contact'))
    return render_template('contact.html')
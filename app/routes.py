from flask import render_template, request, redirect, url_for
from app import app, db
from app.models import BlogPost

@app.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    posts = BlogPost.query.order_by(BlogPost.date_posted.desc()).paginate(page=page, per_page=app.config['POSTS_PER_PAGE'])
    return render_template('index.html', posts=posts)

@app.route('/post/<int:post_id>')
def post(post_id):
    post = BlogPost.query.get_or_404(post_id)
    return render_template('blog_post.html', post=post)

# Diğer rotaları buraya ekleyebilirsiniz (örneğin, yeni blog gönderisi oluşturma)
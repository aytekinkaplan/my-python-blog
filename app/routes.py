from flask import render_template, request, redirect, url_for, flash, jsonify, abort
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.urls import url_parse
from app import app, db
from app.models import BlogPost, BlogPostSection, User
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
    post = BlogPost.query.options(db.joinedload(BlogPost.sections)).get_or_404(post_id)
    print(f"Post content: {post.content}")  # Debug için
    print(f"Number of sections: {len(post.sections)}")  # Debug için
    for section in post.sections:
        print(f"Section title: {section.title}")  # Debug için
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
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        if not all([name, email, message]):
            flash('All fields are required.', 'error')
            return redirect(url_for('contact'))
        # Here you can process the form data (e.g., send an email)
        flash('Your message has been sent successfully!', 'success')
        return redirect(url_for('contact'))
    return render_template('contact.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user is None or not user.check_password(password):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/create_post', methods=['GET', 'POST'])
@login_required
def create_post():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        
        if not title or not content:
            flash('Title and content are required!', 'error')
            return redirect(url_for('create_post'))
        
        new_post = BlogPost(title=title, content=content, author=current_user)
        
        section_titles = request.form.getlist('section_title')
        section_contents = request.form.getlist('section_content')
        section_codes = request.form.getlist('section_code')
        section_outputs = request.form.getlist('section_output')
        
        for i in range(len(section_titles)):
            if section_titles[i]:  # Only add sections with a title
                new_section = BlogPostSection(
                    title=section_titles[i],
                    content=section_contents[i],
                    code=section_codes[i],
                    output=section_outputs[i]
                )
                new_post.sections.append(new_section)
        
        db.session.add(new_post)
        db.session.commit()
        
        flash('Your post has been created!', 'success')
        return redirect(url_for('post', post_id=new_post.id))
    
    return render_template('create_post.html')

@app.route('/post/<int:post_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    post = BlogPost.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    if request.method == 'POST':
        post.title = request.form.get('title')
        post.content = request.form.get('content')
        
        if not post.title or not post.content:
            flash('Title and content are required!', 'error')
            return redirect(url_for('edit_post', post_id=post.id))
        
        # Mevcut bölümleri güncelle veya sil
        existing_section_ids = set()
        for key in request.form:
            if key.startswith('section_title_'):
                section_id = int(key.split('_')[-1])
                existing_section_ids.add(section_id)
                section = BlogPostSection.query.get(section_id)
                if section:
                    section.title = request.form.get(f'section_title_{section_id}')
                    section.content = request.form.get(f'section_content_{section_id}')
                    section.code = request.form.get(f'section_code_{section_id}')
                    section.output = request.form.get(f'section_output_{section_id}')
        
        # Silinmesi gereken bölümleri sil
        for section in post.sections[:]:
            if section.id not in existing_section_ids:
                db.session.delete(section)
                post.sections.remove(section)
        
        # Yeni bölümler ekle
        new_section_titles = request.form.getlist('new_section_title')
        new_section_contents = request.form.getlist('new_section_content')
        new_section_codes = request.form.getlist('new_section_code')
        new_section_outputs = request.form.getlist('new_section_output')
        
        for i in range(len(new_section_titles)):
            if new_section_titles[i]:
                new_section = BlogPostSection(
                    title=new_section_titles[i],
                    content=new_section_contents[i],
                    code=new_section_codes[i],
                    output=new_section_outputs[i]
                )
                post.sections.append(new_section)
        
        db.session.commit()
        
        # Debug için
        print(f"Updated post content: {post.content}")
        print(f"Number of sections after update: {len(post.sections)}")
        for section in post.sections:
            print(f"Updated section title: {section.title}")
        
        flash('Your post has been updated!', 'success')
        return redirect(url_for('post', post_id=post.id))
    
    return render_template('edit_post.html', post=post)

@app.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    post = BlogPost.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('index'))

@app.route('/forgot_password')
def forgot_password():
    # Şimdilik basit bir mesaj gösterelim
    return "Forgot Password functionality will be implemented soon."

@app.route('/register')
def register():
    # Şimdilik basit bir mesaj gösterelim
    return "User registration functionality will be implemented soon."
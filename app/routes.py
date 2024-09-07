from flask import render_template, request, redirect, url_for, flash, jsonify
from app import app, db
from app.models import BlogPost, BlogPostSection
from config import Config

@app.route('/')
@app.route('/page/<int:page>')
def index(page=1):
    posts = BlogPost.query.order_by(BlogPost.date_posted.asc()).paginate(
        page=page, 
        per_page=Config.POSTS_PER_PAGE,
        error_out=False
    )
    return render_template('index.html', posts=posts)

@app.route('/post/<int:post_id>')
def post(post_id):
    post = BlogPost.query.options(db.joinedload(BlogPost.sections)).get_or_404(post_id)
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

@app.route('/create_post', methods=['GET', 'POST'])
def create_post():
    if request.method == 'POST':
        data = request.json
        new_post = BlogPost(title=data['title'], content=data['content'])
        for section in data['sections']:
            new_post.sections.append(BlogPostSection(
                title=section['title'],
                content=section['content'],
                code=section['code'],
                output=section['output']
            ))
        db.session.add(new_post)
        db.session.commit()
        return jsonify({"message": "Post created successfully", "id": new_post.id})
    return render_template('create_post.html')

@app.route('/post/<int:post_id>/edit', methods=['GET', 'POST'])
def edit_post(post_id):
    post = BlogPost.query.get_or_404(post_id)
    if request.method == 'POST':
        post.title = request.form['title']
        post.content = request.form['content']
        
        # Mevcut bölümleri güncelle veya sil
        for section in post.sections:
            section_id = str(section.id)
            if section_id in request.form:
                section.title = request.form[f'section_title_{section_id}']
                section.content = request.form[f'section_content_{section_id}']
                section.code = request.form[f'section_code_{section_id}']
                section.output = request.form[f'section_output_{section_id}']
            else:
                db.session.delete(section)
        
        # Yeni bölümler ekle
        new_sections = request.form.getlist('new_section_title')
        for i, title in enumerate(new_sections):
            if title:  # Boş başlıkları atla
                new_section = BlogPostSection(
                    title=title,
                    content=request.form.getlist('new_section_content')[i],
                    code=request.form.getlist('new_section_code')[i],
                    output=request.form.getlist('new_section_output')[i]
                )
                post.sections.append(new_section)
        
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('post', post_id=post.id))
    return render_template('edit_post.html', post=post)

@app.route('/post/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    post = BlogPost.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('index'))
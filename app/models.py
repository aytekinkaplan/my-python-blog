from app import db
from datetime import datetime

class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    sections = db.relationship('BlogPostSection', backref='post', lazy=True)

    def __repr__(self):
        return f"BlogPost('{self.title}', '{self.date_posted}')"

class BlogPostSection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    code = db.Column(db.Text)
    output = db.Column(db.Text)
    post_id = db.Column(db.Integer, db.ForeignKey('blog_post.id'), nullable=False)

    def __repr__(self):
        return f"BlogPostSection('{self.title}')"
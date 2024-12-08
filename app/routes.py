from flask import Blueprint, render_template, request, flash, redirect, url_for
from app.models import BlogPost
from app import db
from datetime import datetime

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('home.html')

@main.route('/blog', methods=['GET', 'POST'])
def blog():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        
        if title and content:
            try:
                new_post = BlogPost(title=title, content=content)
                db.session.add(new_post)
                db.session.commit()
                flash('Your post has been created successfully!', 'success')
            except Exception as e:
                db.session.rollback()
                flash('An error occurred while creating your post. Please try again.', 'error')
                print(f"Database error: {str(e)}")
        else:
            flash('Title and content are required!', 'error')
        
        return redirect(url_for('main.blog'))
    
    # GET request - display blog posts
    try:
        posts = BlogPost.query.order_by(BlogPost.date_posted.desc()).all()
    except Exception as e:
        posts = []
        flash('Unable to load blog posts.', 'error')
        print(f"Database error: {str(e)}")
    
    return render_template('blog.html', posts=posts)
@main.route('/store')
def store():
    return render_template('store.html')

@main.route('/about')
def about():
    return render_template('about.html')

@main.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        
        # Add contact form processing logic here
        
        flash('Thank you for your message! We will get back to you soon.', 'success')
        return redirect(url_for('main.contact'))
    
    return render_template('contact.html')

@main.context_processor
def inject_year():
    return {'year': datetime.now().year}
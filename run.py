from app import app, db
import os

if __name__ == '__main__':
    print("Current working directory:", os.getcwd())
    print("Static folder absolute path:", os.path.abspath(app.static_folder))
    print("Static folder exists:", os.path.exists(app.static_folder))
    
    css_path = os.path.join(app.static_folder, 'css', 'style.css')
    js_path = os.path.join(app.static_folder, 'js', 'script.js')
    
    print("CSS file path:", css_path)
    print("CSS file exists:", os.path.exists(css_path))
    print("JS file path:", js_path)
    print("JS file exists:", os.path.exists(js_path))
    
    with app.app_context():
        db.create_all()
    app.run(debug=True)
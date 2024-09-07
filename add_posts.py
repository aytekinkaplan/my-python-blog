import os
import json
from app import app, db
from app.models import BlogPost

# Get all JSON files in the directory
json_folder = 'allPostsInJSON'
json_files = [f for f in os.listdir(json_folder) if f.endswith('.json')]

with app.app_context():
    db.drop_all()
    db.create_all()

    total_posts_added = 0

    for json_file in json_files:
        json_path = os.path.join(json_folder, json_file)

        # Open and load the JSON file
        with open(json_path, 'r') as f:
            post_data_list = json.load(f)  # This should be a list of blog posts

            # Ensure it's a list of posts and iterate through each post
            if isinstance(post_data_list, list):  # Check if post_data_list is a list
                for post_data in post_data_list:
                    if isinstance(post_data, dict):  # Ensure each item is a dictionary
                        post = BlogPost(
                            title=post_data.get('title', 'Untitled'),
                            content=post_data.get('content', ''),
                            code=post_data.get('code', ''),
                            output=post_data.get('output', '')
                        )
                        db.session.add(post)
                        total_posts_added += 1

    db.session.commit()

print(f"{total_posts_added} blog posts were successfully added from the JSON files!")
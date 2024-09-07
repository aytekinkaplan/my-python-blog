from app import app, db
from app.models import BlogPost

with app.app_context():
    db.drop_all()
    db.create_all()

#     posts = [
#         BlogPost(
#             title='Understanding Python Lists',
#             content='Python lists are versatile data structures that can hold multiple items. They are ordered, mutable, and allow duplicate elements.',
#             code="""
# # Creating a list
# fruits = ['apple', 'banana', 'cherry']

# # Accessing elements
# print(fruits[0])  # Output: apple

# # Modifying elements
# fruits[1] = 'blueberry'
# print(fruits)  # Output: ['apple', 'blueberry', 'cherry']

# # Adding elements
# fruits.append('date')
# print(fruits)  # Output: ['apple', 'blueberry', 'cherry', 'date']
#             """,
#             output="""
# apple
# ['apple', 'blueberry', 'cherry']
# ['apple', 'blueberry', 'cherry', 'date']
#             """
#         ),
#         # Add more posts here...
#     ]

    for post in posts:
        db.session.add(post)

    db.session.commit()

print(f"{len(posts)} blog posts have been added successfully!")
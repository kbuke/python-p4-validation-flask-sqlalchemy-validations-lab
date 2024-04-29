from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()
    
class Author(db.Model):
    __tablename__ = 'authors'

    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators 
    @validates('name')
    def validate_author_name(self, key, name):
        if not name:
            raise ValueError('Author must have a name')
        author_name_duplicate = Author.query.filter_by(name=name).first()
        if author_name_duplicate:
            raise ValueError("No authors can share a name")
        return name
    
    @validates('phone_number')
    def validate_author_number(self, key, phone_number):
        if len(phone_number) != 10 or not phone_number.isdigit():
            raise ValueError("Phone number must be 10 digits")
        return phone_number

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators  
    @validates("title")
    def validate_post_title(self, key, title):
        print(title)
        if not title:
            raise ValueError('Post must have a title')
        restricted_words = ["Won't Believe", "Secret", "Top", "Guess"]
        if any(word in title for word in restricted_words):
            return title
        raise ValueError('Title must include one of the resricted words')

    @validates('content')
    def validate_post_content(self, key, content):
        if not content or len(content) < 250:
            raise ValueError("Post must be atleast 250 characthers")
        return content
    
    @validates("summary")
    def validate_post_summary(self, key, summary):
        if len(summary) > 250:
            raise ValueError("Summary can be maximum 250 characters")
        return summary
    
    @validates('category')
    def validate_post_category(self, key, category):
        if category != "Fiction" and category != "Non-Fiction":
            raise ValueError("Category must be either Fiction or Non-Fiction")
        return category

    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'

from app import db


class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.String(255))
    color = db.Column(db.String(7), default='#007BFF')

    def __repr__(self):
        return f'<Category {self.name}>'

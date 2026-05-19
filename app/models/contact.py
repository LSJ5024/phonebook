from datetime import datetime
from app import db

contact_categories = db.Table('contact_categories',
    db.Column('contact_id', db.Integer, db.ForeignKey('contacts.id'), primary_key=True),
    db.Column('category_id', db.Integer, db.ForeignKey('categories.id'), primary_key=True)
)

contact_tags = db.Table('contact_tags',
    db.Column('contact_id', db.Integer, db.ForeignKey('contacts.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'), primary_key=True)
)


class Contact(db.Model):
    __tablename__ = 'contacts'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, index=True)
    phone = db.Column(db.String(30))
    mobile = db.Column(db.String(30))
    email = db.Column(db.String(120), index=True)
    organization = db.Column(db.String(150), index=True)
    department = db.Column(db.String(100))
    position = db.Column(db.String(100))
    address = db.Column(db.String(255))
    memo = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    categories = db.relationship('Category', secondary=contact_categories,
                                 lazy='subquery', backref=db.backref('contacts', lazy=True))
    tags = db.relationship('Tag', secondary=contact_tags,
                           lazy='subquery', backref=db.backref('contacts', lazy=True))

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'phone': self.phone,
            'mobile': self.mobile,
            'email': self.email,
            'organization': self.organization,
            'department': self.department,
            'position': self.position,
            'address': self.address,
            'memo': self.memo,
            'categories': [c.name for c in self.categories],
            'tags': [t.name for t in self.tags],
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }

    def __repr__(self):
        return f'<Contact {self.name}>'

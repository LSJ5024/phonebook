from datetime import datetime
from app import db


class AuditLog(db.Model):
    __tablename__ = 'audit_logs'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    action = db.Column(db.String(50), nullable=False)   # 'login', 'logout', 'create', 'update', 'delete', 'export'
    target_type = db.Column(db.String(50))              # 'contact', 'user', 'category'
    target_id = db.Column(db.Integer)
    description = db.Column(db.String(255))
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    def __repr__(self):
        return f'<AuditLog {self.action} by user {self.user_id}>'

import os
import functools
from datetime import datetime
from flask import request, abort
from flask_login import current_user
from app import db
from app.models.audit_log import AuditLog


def log_action(action, target_type=None, target_id=None, description=None):
    """사용자 활동을 AuditLog에 기록한다."""
    entry = AuditLog(
        user_id=current_user.id if current_user.is_authenticated else None,
        action=action,
        target_type=target_type,
        target_id=target_id,
        description=description,
        ip_address=request.remote_addr,
        user_agent=request.user_agent.string[:255] if request.user_agent.string else None,
    )
    db.session.add(entry)
    db.session.commit()


def admin_required(f):
    """관리자 전용 라우트 데코레이터."""
    @functools.wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            abort(403)
        return f(*args, **kwargs)
    return decorated


def allowed_file(filename, allowed_extensions=None):
    if allowed_extensions is None:
        allowed_extensions = {'csv', 'xlsx', 'xls'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions


def parse_import_file(filepath):
    """CSV/Excel 파일을 파싱하여 dict 리스트를 반환한다."""
    import pandas as pd
    ext = os.path.splitext(filepath)[1].lower()
    if ext == '.csv':
        df = pd.read_csv(filepath, encoding='utf-8-sig')
    else:
        df = pd.read_excel(filepath)

    df.columns = [c.strip().lower() for c in df.columns]
    return df.where(df.notna(), None).to_dict(orient='records')


COLUMN_MAP = {
    'name': 'name', '이름': 'name',
    'phone': 'phone', '전화번호': 'phone',
    'mobile': 'mobile', '휴대폰': 'mobile',
    'email': 'email', '이메일': 'email',
    'organization': 'organization', '소속': 'organization',
    'department': 'department', '부서': 'department',
    'position': 'position', '직책': 'position',
    'address': 'address', '주소': 'address',
    'memo': 'memo', '메모': 'memo',
}

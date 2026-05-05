# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 프로젝트 개요

기업/기관용 웹 기반 전화번호 관리 시스템. Flask(Python) 백엔드 + Bootstrap5 프론트엔드, MySQL 연동.

## 개발 환경 설정

```bash
# 가상환경 생성 및 활성화
python -m venv venv
source venv/bin/activate        # Linux/Mac
venv\Scripts\activate           # Windows

# 의존성 설치
pip install -r requirements.txt

# DB 마이그레이션
flask db init
flask db migrate -m "Initial migration"
flask db upgrade

# 앱 실행
python run.py
```

서버 기본 주소: http://localhost:5000

## 데이터베이스 접속 정보

`config/config.py`에서 관리:

```
Host: 203.255.78.58  Port: 9003  User: user1  Password: 123  DB: phonebook
```

MySQL 인코딩: `utf8mb4 / utf8mb4_unicode_ci`

## 기술 스택

| 구분 | 기술 |
|------|------|
| 백엔드 | Python 3.9+, Flask 2.3 |
| ORM / 마이그레이션 | Flask-SQLAlchemy 3, Flask-Migrate 4 |
| 인증 | Flask-Login, PyJWT, Werkzeug(bcrypt 해싱) |
| 폼 검증 | Flask-WTF |
| 다국어 | Flask-Babel (한국어/영어) |
| 이메일 | Flask-Mail |
| Import/Export | pandas, openpyxl, xlrd, xlsxwriter |
| 프론트엔드 | HTML5, Bootstrap 5, jQuery, Font Awesome |
| 환경변수 | python-dotenv |

## 아키텍처

Flask **Application Factory** 패턴 사용 권장:

```
phonebookcc/
├── app/
│   ├── __init__.py          # create_app() 팩토리
│   ├── models/              # SQLAlchemy 모델 (User, Contact, Category, Tag, AuditLog)
│   ├── views/               # Blueprint별 라우트
│   │   ├── auth.py          # 로그인/회원가입/비밀번호 찾기
│   │   ├── contacts.py      # 연락처 CRUD + 검색/필터
│   │   ├── admin.py         # 사용자 권한, 시스템 로그
│   │   └── api.py           # RESTful JSON API
│   ├── forms/               # Flask-WTF 폼 클래스
│   ├── static/              # CSS, JS, 이미지
│   └── templates/           # Jinja2 템플릿
│       └── admin/
├── config/
│   └── config.py            # DB 접속 정보, 앱 설정
├── migrations/              # Flask-Migrate 자동 생성
├── run.py                   # 앱 진입점
└── requirements.txt
```

## 핵심 도메인 모델

- **User**: 이메일/비밀번호 인증, `role` 필드로 admin/user 구분, 첫 가입자 자동 admin 부여
- **Contact**: 이름·전화번호·이메일·소속·메모 필드, 다대다 Tag 관계
- **Category**: 부서/팀/프로젝트 단위 분류, Contact와 다대다
- **Tag**: 유연한 다중 분류, Contact와 다대다
- **AuditLog**: 사용자 활동 기록 (IP, 타임스탬프, 액션)

## 다국어 처리

- `Flask-Babel` 사용, 언어 파일: `app/translations/ko/`, `app/translations/en/`
- 템플릿 내 `{{ _('문자열') }}` 래핑
- 세션 또는 URL 파라미터로 언어 전환
- `pybabel extract / update / compile` 워크플로우

## 보안 요구사항

- 비밀번호: `werkzeug.security.generate_password_hash` (bcrypt)
- SQL Injection: SQLAlchemy ORM 사용으로 원천 차단, raw query 금지
- CSRF: Flask-WTF가 모든 POST 폼 보호 (`{{ form.hidden_tag() }}` 필수)
- 파일 업로드: 확장자·MIME 타입 검증 후 저장
- 관리자 전용 라우트: `@login_required` + `@admin_required` 데코레이터 적용

## Import/Export 처리

- CSV/Excel 업로드 → `pandas.read_csv` / `read_excel` 파싱 → bulk insert
- 내보내기: `xlsxwriter`로 Excel 생성, `StringIO`로 CSV 스트리밍 응답
- 백업/복원(관리자 전용): JSON 전체 덤프 방식 고려

## UI/UX 가이드라인

- 브랜드 컬러: `#007BFF` (블루) + 화이트/그레이 중립 톤
- 반응형: Bootstrap 5 그리드, 모바일 우선 설계
- 접근성: WAI-ARIA 속성, 키보드 내비게이션, 색상 대비 4.5:1 이상
- 헤더: 로고, 로그인/로그아웃, 언어 전환 버튼
- 푸터: 시스템 정보, 개인정보 처리방침, 문의 이메일

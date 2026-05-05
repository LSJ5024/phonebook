# PhoneBook - 전화번호 관리 시스템

기업 또는 기관이 구성원 및 관련 인물의 연락처를 안전하고 효율적으로 관리할 수 있도록 지원하는 웹 애플리케이션입니다.

## 주요 기능

- 사용자 인증 및 권한 관리 시스템
- 연락처 CRUD 기능 (생성, 조회, 수정, 삭제)
- 카테고리 및 태그를 통한 연락처 분류
- 다양한 검색 및 필터링 옵션
- 다국어 지원 (한국어, 영어)
- CSV/Excel 가져오기/내보내기 기능
- 백업 및 복원 기능
- 사용자 활동 로깅 및 감사

## 기술 스택

### 백엔드
- Python 3.9+
- Flask 웹 프레임워크
- SQLAlchemy ORM
- MySQL 데이터베이스
- Flask 확장 모듈:
  - Flask-Login (인증)
  - Flask-WTF (폼 처리)
  - Flask-Babel (다국어)
  - Flask-Mail (이메일)

### 프론트엔드
- HTML5, CSS3, JavaScript
- Bootstrap 5
- Font Awesome
- jQuery

## 시스템 요구사항

- Python 3.9+
- MySQL 5.7+
- pip (Python 패키지 관리자)
- 가상 환경 (venv 또는 virtualenv)

## 설치 방법

### 1. 저장소 복제

```bash
git clone https://github.com/yourusername/phonebook.git
cd phonebook
```

### 2. 가상 환경 설정

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 또는 
venv\Scripts\activate  # Windows
```

### 3. 의존성 설치

```bash
pip install -r requirements.txt
```

### 4. 데이터베이스 설정

MySQL에서 새 데이터베이스 생성:

```sql
CREATE DATABASE phonebook CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

`config/config.py` 파일에서 데이터베이스 연결 정보 수정:

```python
MYSQL_HOST = '203.255.78.58'  # 필요에 따라 변경
MYSQL_PORT = 9003             # 필요에 따라 변경
MYSQL_USER = 'user1'          # 필요에 따라 변경
MYSQL_PASSWORD = '123'        # 필요에 따라 변경
MYSQL_DB = 'phonebook'
```

### 5. 데이터베이스 마이그레이션

```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

### 6. 애플리케이션 실행

```bash
python run.py
```

애플리케이션은 기본적으로 http://localhost:5000 에서 실행됩니다.

## 사용자 가이드

### 초기 관리자 계정 설정

처음 애플리케이션을 실행하고 첫 번째 사용자 계정을 등록하면 자동으로 관리자 권한이 부여됩니다.

### 연락처 관리

- **연락처 추가**: "Contacts" > "Add New" 메뉴를 통해 새 연락처 추가
- **연락처 검색**: 상단 검색창을 통해 이름, 전화번호, 이메일, 소속 등으로 검색
- **연락처 필터링**: 카테고리 또는 태그로 연락처 필터링

### 데이터 가져오기/내보내기

- **가져오기**: "Import Contacts" 메뉴를 통해 CSV 또는 Excel 파일 업로드
- **내보내기**: "Export as CSV/Excel" 옵션을 통해 연락처 내보내기

### 백업 및 복원 (관리자 전용)

- **백업**: "Admin" > "Backup & Restore" > "Full Backup" 버튼 클릭
- **복원**: "Admin" > "Backup & Restore" > "Import Data" 에서 백업 파일 업로드

## 개발자 정보

이 프로젝트는 요청사항에 따라 개발되었습니다. 자세한 정보나 지원이 필요한 경우 다음 연락처로 문의하세요:

- 이메일: contact@example.com
- 전화: 02-123-4567

## 라이센스

이 프로젝트는 MIT 라이센스에 따라 배포됩니다. 자세한 내용은 LICENSE 파일을 참조하세요.
# 전화번호부 (Sad Phonebook)

이름과 전화번호를 등록·수정·삭제할 수 있는 심플한 전화번호부 웹 앱.

## 기술 스택

- **Frontend**: React + Vite + Tailwind CSS v4
- **Database**: Supabase (PostgreSQL)
- **Deploy**: Vercel

## 로컬 실행

```bash
npm install
# .env 파일에 Supabase 환경변수 입력
npm run dev
```

## 환경변수

`.env.example`을 참고하여 `.env` 파일을 생성하세요.

```
VITE_SUPABASE_URL=your_supabase_project_url
VITE_SUPABASE_ANON_KEY=your_supabase_anon_key
```

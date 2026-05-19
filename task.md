# Task — 전화번호부 (Sad Phonebook)

## 진행 상태 범례
- [ ] 미완료
- [x] 완료

---

## Phase 1. 프로젝트 초기 설정

- [x] **T-01** Vite + React 프로젝트 생성
- [x] **T-02** Tailwind CSS 설치 및 설정 (v4, @tailwindcss/vite 플러그인)
- [x] **T-03** Supabase 클라이언트 패키지 설치
- [x] **T-04** 환경변수 파일 설정 (`.env`, `.env.example`, `.gitignore` 추가)
- [ ] **T-05** Vercel 프로젝트 연결
  - GitHub 레포 푸시 후 Vercel에서 프로젝트 연결
  - Vercel 환경변수 등록 (`VITE_SUPABASE_URL`, `VITE_SUPABASE_ANON_KEY`)

---

## Phase 2. Supabase 설정

- [x] **T-06** Supabase 프로젝트 생성
- [x] **T-07** `contacts` 테이블 생성
- [x] **T-08** Row Level Security (RLS) 설정

- [x] **T-09** Supabase 클라이언트 모듈 작성 (`src/lib/supabase.js`)

---

## Phase 3. 핵심 기능 구현

- [x] **T-10** 연락처 목록 조회 (`READ`) — 로딩 상태 포함
- [x] **T-11** 연락처 등록 (`CREATE`) — 필수값 검증 포함
- [x] **T-12** 연락처 수정 (`UPDATE`) — 인라인 편집
- [x] **T-13** 연락처 삭제 (`DELETE`) — 확인 다이얼로그 포함

---

## Phase 4. UI 마무리

- [x] **T-14** 반응형 레이아웃 적용 (Tailwind 반응형 유틸리티)
- [x] **T-15** 빈 목록 상태 (Empty State) 처리
- [x] **T-16** 에러 상태 처리

---

## Phase 5. 배포 및 검증

- [x] **T-17** 빌드 검증 (`npm run build` 통과)
- [ ] **T-18** Vercel 배포 확인
  - 배포 후 실제 URL에서 CRUD 전체 동작 확인
- [ ] **T-19** 최종 점검
  - 모바일 브라우저에서 동작 확인
  - 빈 값 제출, 연속 삭제 등 엣지 케이스 검증

---

## 의존 관계

```
T-01 → T-02 → T-03 → T-04
T-06 → T-07 → T-08 → T-09
T-04, T-09 → T-10 → T-11 → T-12 → T-13
T-13 → T-14 → T-15 → T-16
T-16 → T-05 → T-17 → T-18 → T-19
```

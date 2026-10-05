# MVP Phase 1

## Day 1

- [x] 프로젝트 기본 폴더 구조 생성
- [x] Git 초기화
- [x] README 생성
- [x] AGENTS.md 생성
- [x] docs 기본 구조 생성
- [x] docs/ROADMAP.md 생성
- [x] docs/DATABASE.md 생성
- [x] docs/API.md 생성
- [x] docs/ARCHITECTURE.md 생성

## Day 2

- [x] PostgreSQL Docker 컨테이너 실행
- [x] relay 데이터베이스 생성
- [x] Master 테이블 DDL 작성
- [x] departments 테이블 생성
- [x] users 테이블 생성
- [x] code_groups 테이블 생성
- [x] common_codes 테이블 생성
- [x] roles 테이블 생성
- [x] user_roles 테이블 생성
- [x] applications 테이블 생성
- [x] PK / FK / UNIQUE / INDEX 구성
- [x] Master Seed Data 작성
- [x] 테스트 사용자 / 부서 / 역할 데이터 입력
- [x] PostgreSQL 데이터 조회 검증

## Day 3

- [x] Python 가상환경 생성
- [x] FastAPI 기본 프로젝트 생성
- [x] PostgreSQL 연결 설정
- [x] SQLAlchemy 설정
- [x] Pydantic Settings 환경변수 구성
- [x] Alembic 패키지 설치
- [x] `/health` API 구현
- [x] PostgreSQL 연결 상태 확인
- [x] FastAPI Swagger 확인

## Day 4

- [x] User / Department SQLAlchemy Model 생성
- [x] Pydantic Response Schema 생성
- [x] Repository 계층 구현
- [x] Service 계층 구현
- [x] Router 계층 구현
- [x] DB Session 의존성 주입 (`Depends`)
- [x] GET `/api/users`
- [x] GET `/api/users/{user_id}`
- [x] GET `/api/departments`
- [x] PostgreSQL Seed Data 조회 테스트

## Day 5

- [x] 인증 관련 패키지 설치
- [x] JWT 환경변수 설정
- [x] 비밀번호 해싱 및 검증 함수 구현
- [x] 테스트 계정 비밀번호 해시 적용
- [x] 이메일 기반 사용자 조회 기능
- [x] Auth Request / Response Schema 생성
- [x] 로그인 Service 및 Router 구현
- [x] POST `/api/auth/login`
- [x] JWT Access Token 발급 테스트
- [x] React + TypeScript + Vite 프로젝트 생성
- [x] ESLint 초기 설정

## Day 6

- [x] React Router 설치
- [x] Axios 설치
- [x] 공통 API Client 생성
- [x] LoginPage 구현
- [x] 로그인 API 연동
- [x] JWT localStorage 저장
- [x] MainLayout 구현
- [x] Header 컴포넌트 구현
- [x] Sidebar 컴포넌트 구현
- [x] DashboardPage 생성
- [x] Router 및 Outlet 구성
- [x] FastAPI CORS 설정
- [x] 로그인 후 Dashboard 이동
- [x] 로그아웃 기능 구현
- [x] 비로그인 사용자 `/login` 리다이렉트
- [x] 새로고침 후 로그인 상태 유지 확인

## Day 7 — Frontend Polish

- [x] Relay 브랜드 이미지 추가
- [x] Light Mode용 Relay 로고 추가
- [x] Dark Mode용 Relay 로고 추가
- [x] Relay Symbol / App Icon 추가
- [x] Favicon 변경
- [x] 브라우저 Title 변경
- [x] LoginPage Relay 브랜딩 적용
- [x] Sidebar Relay 로고 적용
- [x] 로그인 아이디 저장 기능
- [x] 저장된 이메일 자동 불러오기
- [x] 기본 테스트 비밀번호 제거
- [x] Light / Dark 테마 구현
- [x] ThemeContext 생성
- [x] ThemeProvider 생성
- [x] useTheme Custom Hook 생성
- [x] CSS Variables 기반 공통 테마 구성
- [x] 테마 localStorage 저장 및 복원
- [x] 테마별 Relay 로고 자동 변경
- [x] LoginPage 테마 적용
- [x] Dashboard / Layout 테마 적용
- [x] 새로고침 후 테마 유지 확인

## Day 8 — Approval Database & Basic API

- [x] 전자결재 공통코드 Seed 추가
- [x] `approval_documents` 테이블 생성
- [x] `approval_lines` 테이블 생성
- [x] `approval_histories` 테이블 생성
- [x] 결재 관련 FK / INDEX 구성
- [x] ApprovalDocument SQLAlchemy Model 생성
- [x] ApprovalLine SQLAlchemy Model 생성
- [x] ApprovalHistory SQLAlchemy Model 생성
- [x] Approval Request / Response Schema 생성
- [x] Approval Repository 구현
- [x] 공통코드 ID 조회 기능 구현
- [x] Repository `flush()` 기반 저장 구조 적용
- [x] Approval Service 구현
- [x] 결재문서 / 결재선 / 이력 단일 Transaction 처리
- [x] 실패 시 Rollback 처리
- [x] POST `/api/approvals` 구현
- [x] Swagger 결재문서 생성 테스트
- [x] DBeaver에서 결재문서 1건 / 결재선 2건 / 이력 1건 저장 확인

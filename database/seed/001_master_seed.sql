/* =========================================================
   Relay - Master Seed Data
   File: 001_master_seed.sql
   ========================================================= */


/* =========================================================
   1. code_groups
   ========================================================= */

INSERT INTO code_groups (code, name, description)
VALUES
('POSITION', '직급', '임직원 직급'),
('JOB_TITLE', '직책', '임직원 직책'),
('USER_STATUS', '사용자 상태', '재직 상태'),
('APPLICATION_STATUS', '프로그램 상태', '사내 프로그램 운영 상태');


/* =========================================================
   2. common_codes
   ========================================================= */

-- POSITION
INSERT INTO common_codes (group_id, code, name, sort_order)
SELECT id, 'STAFF', '사원', 1
FROM code_groups
WHERE code = 'POSITION';

INSERT INTO common_codes (group_id, code, name, sort_order)
SELECT id, 'ASSISTANT_MANAGER', '대리', 2
FROM code_groups
WHERE code = 'POSITION';

INSERT INTO common_codes (group_id, code, name, sort_order)
SELECT id, 'MANAGER', '과장', 3
FROM code_groups
WHERE code = 'POSITION';

INSERT INTO common_codes (group_id, code, name, sort_order)
SELECT id, 'DEPUTY_MANAGER', '차장', 4
FROM code_groups
WHERE code = 'POSITION';

INSERT INTO common_codes (group_id, code, name, sort_order)
SELECT id, 'GENERAL_MANAGER', '부장', 5
FROM code_groups
WHERE code = 'POSITION';


-- JOB_TITLE
INSERT INTO common_codes (group_id, code, name, sort_order)
SELECT id, 'MEMBER', '팀원', 1
FROM code_groups
WHERE code = 'JOB_TITLE';

INSERT INTO common_codes (group_id, code, name, sort_order)
SELECT id, 'TEAM_LEADER', '팀장', 2
FROM code_groups
WHERE code = 'JOB_TITLE';

INSERT INTO common_codes (group_id, code, name, sort_order)
SELECT id, 'DIVISION_LEADER', '본부장', 3
FROM code_groups
WHERE code = 'JOB_TITLE';


-- USER_STATUS
INSERT INTO common_codes (group_id, code, name, sort_order)
SELECT id, 'ACTIVE', '재직', 1
FROM code_groups
WHERE code = 'USER_STATUS';

INSERT INTO common_codes (group_id, code, name, sort_order)
SELECT id, 'ON_LEAVE', '휴직', 2
FROM code_groups
WHERE code = 'USER_STATUS';

INSERT INTO common_codes (group_id, code, name, sort_order)
SELECT id, 'RESIGNED', '퇴사', 3
FROM code_groups
WHERE code = 'USER_STATUS';


-- APPLICATION_STATUS
INSERT INTO common_codes (group_id, code, name, sort_order)
SELECT id, 'OPERATING', '운영중', 1
FROM code_groups
WHERE code = 'APPLICATION_STATUS';

INSERT INTO common_codes (group_id, code, name, sort_order)
SELECT id, 'MAINTENANCE', '점검중', 2
FROM code_groups
WHERE code = 'APPLICATION_STATUS';

INSERT INTO common_codes (group_id, code, name, sort_order)
SELECT id, 'SUSPENDED', '중지', 3
FROM code_groups
WHERE code = 'APPLICATION_STATUS';

INSERT INTO common_codes (group_id, code, name, sort_order)
SELECT id, 'RETIRED', '운영종료', 4
FROM code_groups
WHERE code = 'APPLICATION_STATUS';


/* =========================================================
   3. departments
   ========================================================= */

INSERT INTO departments (code, name, sort_order)
VALUES
('DEP_DEV', '개발본부', 1),
('DEP_SUPPORT', '경영지원본부', 2);

INSERT INTO departments (code, name, parent_id, sort_order)
SELECT 'DEP_EMR', 'EMR팀', id, 1
FROM departments
WHERE code = 'DEP_DEV';

INSERT INTO departments (code, name, parent_id, sort_order)
SELECT 'DEP_PLATFORM', '플랫폼팀', id, 2
FROM departments
WHERE code = 'DEP_DEV';

INSERT INTO departments (code, name, parent_id, sort_order)
SELECT 'DEP_HR', '인사팀', id, 1
FROM departments
WHERE code = 'DEP_SUPPORT';


/* =========================================================
   4. roles
   ========================================================= */

INSERT INTO roles (code, name, description, is_system)
VALUES
('EMPLOYEE', '일반 사용자', '기본 사용자 역할', TRUE),
('MANAGER', '관리자', '결재 및 팀 관리 역할', TRUE),
('DEVELOPER', '개발자', '개발 요청 처리 역할', TRUE),
('HR_ADMIN', '인사 관리자', '인사 및 연차 관리 역할', TRUE),
('SYSTEM_ADMIN', '시스템 관리자', '전체 시스템 관리자', TRUE);


/* =========================================================
   5. users
   ========================================================= */

-- 비밀번호는 아직 실제 해시가 아님.
-- Day 5 인증 구현 시 BCrypt/Argon2 해시로 변경 예정.

INSERT INTO users (
    employee_no,
    email,
    password_hash,
    name,
    birth_date,
    department_id,
    position_id,
    job_title_id,
    status_id,
    join_date
)
SELECT
    'EMP0001',
    'admin@relay.local',
    'TEMP_PASSWORD',
    '시스템관리자',
    DATE '1990-01-01',
    d.id,
    p.id,
    j.id,
    s.id,
    DATE '2026-01-01'
FROM departments d
JOIN common_codes p ON p.code = 'GENERAL_MANAGER'
JOIN common_codes j ON j.code = 'TEAM_LEADER'
JOIN common_codes s ON s.code = 'ACTIVE'
WHERE d.code = 'DEP_DEV';


INSERT INTO users (
    employee_no,
    email,
    password_hash,
    name,
    birth_date,
    department_id,
    position_id,
    job_title_id,
    status_id,
    join_date
)
SELECT
    'EMP0002',
    'developer@relay.local',
    'TEMP_PASSWORD',
    '김개발',
    DATE '1993-09-22',
    d.id,
    p.id,
    j.id,
    s.id,
    DATE '2024-03-04'
FROM departments d
JOIN common_codes p ON p.code = 'ASSISTANT_MANAGER'
JOIN common_codes j ON j.code = 'MEMBER'
JOIN common_codes s ON s.code = 'ACTIVE'
WHERE d.code = 'DEP_EMR';


INSERT INTO users (
    employee_no,
    email,
    password_hash,
    name,
    birth_date,
    department_id,
    manager_id,
    position_id,
    job_title_id,
    status_id,
    join_date
)
SELECT
    'EMP0003',
    'employee@relay.local',
    'TEMP_PASSWORD',
    '홍길동',
    DATE '1996-05-15',
    d.id,
    m.id,
    p.id,
    j.id,
    s.id,
    DATE '2025-02-03'
FROM departments d
JOIN users m ON m.email = 'admin@relay.local'
JOIN common_codes p ON p.code = 'STAFF'
JOIN common_codes j ON j.code = 'MEMBER'
JOIN common_codes s ON s.code = 'ACTIVE'
WHERE d.code = 'DEP_EMR';


/* =========================================================
   6. user_roles
   ========================================================= */

INSERT INTO user_roles (user_id, role_id)
SELECT u.id, r.id
FROM users u
JOIN roles r ON r.code = 'EMPLOYEE'
WHERE u.email IN (
    'admin@relay.local',
    'developer@relay.local',
    'employee@relay.local'
);

INSERT INTO user_roles (user_id, role_id)
SELECT u.id, r.id
FROM users u
JOIN roles r ON r.code = 'SYSTEM_ADMIN'
WHERE u.email = 'admin@relay.local';

INSERT INTO user_roles (user_id, role_id)
SELECT u.id, r.id
FROM users u
JOIN roles r ON r.code = 'MANAGER'
WHERE u.email = 'admin@relay.local';

INSERT INTO user_roles (user_id, role_id)
SELECT u.id, r.id
FROM users u
JOIN roles r ON r.code = 'DEVELOPER'
WHERE u.email = 'developer@relay.local';


/* =========================================================
   7. applications
   ========================================================= */

INSERT INTO applications (
    code,
    name,
    description,
    owner_department_id,
    current_version,
    status_id
)
SELECT
    'APP_EMR',
    'EMR',
    'EMR 업무 시스템',
    d.id,
    '1.0.0',
    s.id
FROM departments d
JOIN common_codes s ON s.code = 'OPERATING'
WHERE d.code = 'DEP_EMR';

INSERT INTO applications (
    code,
    name,
    description,
    owner_department_id,
    current_version,
    status_id
)
SELECT
    'APP_GROUPWARE',
    '그룹웨어',
    '사내 그룹웨어 시스템',
    d.id,
    '1.0.0',
    s.id
FROM departments d
JOIN common_codes s ON s.code = 'OPERATING'
WHERE d.code = 'DEP_PLATFORM';
/* =========================================================
   Relay - Master Tables
   File: 001_master.sql

   생성 순서
   1. departments
   2. code_groups
   3. common_codes
   4. users
   5. roles
   6. user_roles
   7. applications

   주의:
   created_by / updated_by FK는 users 테이블 생성 이후
   별도 ALTER TABLE로 연결한다.
   ========================================================= */


/* =========================================================
   1. departments
   ========================================================= */

CREATE TABLE departments (
    id              BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    code            VARCHAR(50) NOT NULL UNIQUE,
    name            VARCHAR(100) NOT NULL,
    parent_id       BIGINT,
    description     VARCHAR(500),
    sort_order      INTEGER NOT NULL DEFAULT 0,
    is_active       BOOLEAN NOT NULL DEFAULT TRUE,

    created_by      BIGINT,
    created_at      TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_by      BIGINT,
    updated_at      TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);


/* =========================================================
   2. code_groups
   ========================================================= */

CREATE TABLE code_groups (
    id              BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    code            VARCHAR(50) NOT NULL UNIQUE,
    name            VARCHAR(100) NOT NULL,
    description     VARCHAR(500),
    is_active       BOOLEAN NOT NULL DEFAULT TRUE,

    created_by      BIGINT,
    created_at      TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_by      BIGINT,
    updated_at      TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);


/* =========================================================
   3. common_codes
   ========================================================= */

CREATE TABLE common_codes (
    id              BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    group_id        BIGINT NOT NULL,
    code            VARCHAR(50) NOT NULL,
    name            VARCHAR(100) NOT NULL,
    description     VARCHAR(500),
    sort_order      INTEGER NOT NULL DEFAULT 0,
    is_active       BOOLEAN NOT NULL DEFAULT TRUE,

    created_by      BIGINT,
    created_at      TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_by      BIGINT,
    updated_at      TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT uq_common_codes_group_code
        UNIQUE (group_id, code)
);


/* =========================================================
   4. users
   ========================================================= */

CREATE TABLE users (
    id              BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    employee_no     VARCHAR(30) NOT NULL UNIQUE,
    email           VARCHAR(255) NOT NULL UNIQUE,
    password_hash   VARCHAR(255) NOT NULL,
    name            VARCHAR(100) NOT NULL,
    birth_date      DATE,

    department_id   BIGINT,
    manager_id      BIGINT,

    position_id     BIGINT,
    job_title_id    BIGINT,
    status_id       BIGINT,

    join_date       DATE,
    is_active       BOOLEAN NOT NULL DEFAULT TRUE,

    created_by      BIGINT,
    created_at      TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_by      BIGINT,
    updated_at      TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);


/* =========================================================
   5. roles
   ========================================================= */

CREATE TABLE roles (
    id              BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    code            VARCHAR(50) NOT NULL UNIQUE,
    name            VARCHAR(100) NOT NULL,
    description     VARCHAR(500),

    is_system       BOOLEAN NOT NULL DEFAULT FALSE,
    is_active       BOOLEAN NOT NULL DEFAULT TRUE,

    created_by      BIGINT,
    created_at      TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_by      BIGINT,
    updated_at      TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);


/* =========================================================
   6. user_roles
   ========================================================= */

CREATE TABLE user_roles (
    id              BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    user_id         BIGINT NOT NULL,
    role_id         BIGINT NOT NULL,

    is_active       BOOLEAN NOT NULL DEFAULT TRUE,

    created_by      BIGINT,
    created_at      TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_by      BIGINT,
    updated_at      TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT uq_user_roles
        UNIQUE (user_id, role_id)
);


/* =========================================================
   7. applications
   ========================================================= */

CREATE TABLE applications (
    id                      BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    code                    VARCHAR(50) NOT NULL UNIQUE,
    name                    VARCHAR(100) NOT NULL,
    description             VARCHAR(500),

    owner_department_id     BIGINT,
    current_version         VARCHAR(50),
    external_url            VARCHAR(500),
    status_id               BIGINT,

    is_active               BOOLEAN NOT NULL DEFAULT TRUE,

    created_by              BIGINT,
    created_at              TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_by              BIGINT,
    updated_at              TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);


/* =========================================================
   Foreign Keys
   ========================================================= */


/* departments */
ALTER TABLE departments
ADD CONSTRAINT fk_departments_parent
FOREIGN KEY (parent_id)
REFERENCES departments(id);

ALTER TABLE departments
ADD CONSTRAINT fk_departments_created_by
FOREIGN KEY (created_by)
REFERENCES users(id);

ALTER TABLE departments
ADD CONSTRAINT fk_departments_updated_by
FOREIGN KEY (updated_by)
REFERENCES users(id);


/* code_groups */
ALTER TABLE code_groups
ADD CONSTRAINT fk_code_groups_created_by
FOREIGN KEY (created_by)
REFERENCES users(id);

ALTER TABLE code_groups
ADD CONSTRAINT fk_code_groups_updated_by
FOREIGN KEY (updated_by)
REFERENCES users(id);


/* common_codes */
ALTER TABLE common_codes
ADD CONSTRAINT fk_common_codes_group
FOREIGN KEY (group_id)
REFERENCES code_groups(id);

ALTER TABLE common_codes
ADD CONSTRAINT fk_common_codes_created_by
FOREIGN KEY (created_by)
REFERENCES users(id);

ALTER TABLE common_codes
ADD CONSTRAINT fk_common_codes_updated_by
FOREIGN KEY (updated_by)
REFERENCES users(id);


/* users */
ALTER TABLE users
ADD CONSTRAINT fk_users_department
FOREIGN KEY (department_id)
REFERENCES departments(id);

ALTER TABLE users
ADD CONSTRAINT fk_users_manager
FOREIGN KEY (manager_id)
REFERENCES users(id);

ALTER TABLE users
ADD CONSTRAINT fk_users_position
FOREIGN KEY (position_id)
REFERENCES common_codes(id);

ALTER TABLE users
ADD CONSTRAINT fk_users_job_title
FOREIGN KEY (job_title_id)
REFERENCES common_codes(id);

ALTER TABLE users
ADD CONSTRAINT fk_users_status
FOREIGN KEY (status_id)
REFERENCES common_codes(id);

ALTER TABLE users
ADD CONSTRAINT fk_users_created_by
FOREIGN KEY (created_by)
REFERENCES users(id);

ALTER TABLE users
ADD CONSTRAINT fk_users_updated_by
FOREIGN KEY (updated_by)
REFERENCES users(id);


/* roles */
ALTER TABLE roles
ADD CONSTRAINT fk_roles_created_by
FOREIGN KEY (created_by)
REFERENCES users(id);

ALTER TABLE roles
ADD CONSTRAINT fk_roles_updated_by
FOREIGN KEY (updated_by)
REFERENCES users(id);


/* user_roles */
ALTER TABLE user_roles
ADD CONSTRAINT fk_user_roles_user
FOREIGN KEY (user_id)
REFERENCES users(id);

ALTER TABLE user_roles
ADD CONSTRAINT fk_user_roles_role
FOREIGN KEY (role_id)
REFERENCES roles(id);

ALTER TABLE user_roles
ADD CONSTRAINT fk_user_roles_created_by
FOREIGN KEY (created_by)
REFERENCES users(id);

ALTER TABLE user_roles
ADD CONSTRAINT fk_user_roles_updated_by
FOREIGN KEY (updated_by)
REFERENCES users(id);


/* applications */
ALTER TABLE applications
ADD CONSTRAINT fk_applications_department
FOREIGN KEY (owner_department_id)
REFERENCES departments(id);

ALTER TABLE applications
ADD CONSTRAINT fk_applications_status
FOREIGN KEY (status_id)
REFERENCES common_codes(id);

ALTER TABLE applications
ADD CONSTRAINT fk_applications_created_by
FOREIGN KEY (created_by)
REFERENCES users(id);

ALTER TABLE applications
ADD CONSTRAINT fk_applications_updated_by
FOREIGN KEY (updated_by)
REFERENCES users(id);


/* =========================================================
   Indexes
   ========================================================= */

CREATE INDEX idx_users_department
ON users(department_id);

CREATE INDEX idx_users_manager
ON users(manager_id);

CREATE INDEX idx_users_status
ON users(status_id);

CREATE INDEX idx_common_codes_group
ON common_codes(group_id);

CREATE INDEX idx_user_roles_user
ON user_roles(user_id);

CREATE INDEX idx_user_roles_role
ON user_roles(role_id);

CREATE INDEX idx_applications_department
ON applications(owner_department_id);

CREATE INDEX idx_applications_status
ON applications(status_id);
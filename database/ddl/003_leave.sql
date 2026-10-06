CREATE TABLE leave_requests (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    approval_document_id BIGINT NOT NULL,
    user_id BIGINT NOT NULL,
    leave_type_id BIGINT NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    days NUMERIC(5,2) NOT NULL,
    reason VARCHAR(500),
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_by BIGINT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_by BIGINT,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_leave_requests_approval_document
        FOREIGN KEY (approval_document_id)
        REFERENCES approval_documents(id),

    CONSTRAINT fk_leave_requests_user
        FOREIGN KEY (user_id)
        REFERENCES users(id),

    CONSTRAINT fk_leave_requests_leave_type
        FOREIGN KEY (leave_type_id)
        REFERENCES common_codes(id),

    CONSTRAINT fk_leave_requests_created_by
        FOREIGN KEY (created_by)
        REFERENCES users(id),

    CONSTRAINT fk_leave_requests_updated_by
        FOREIGN KEY (updated_by)
        REFERENCES users(id)
);

CREATE INDEX idx_leave_requests_user_id
    ON leave_requests(user_id);

CREATE INDEX idx_leave_requests_approval_document_id
    ON leave_requests(approval_document_id);

CREATE INDEX idx_leave_requests_start_date
    ON leave_requests(start_date);


CREATE TABLE leave_balances (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id BIGINT NOT NULL,
    year INTEGER NOT NULL,
    total_days NUMERIC(5,2) NOT NULL DEFAULT 0,
    used_days NUMERIC(5,2) NOT NULL DEFAULT 0,
    remaining_days NUMERIC(5,2) NOT NULL DEFAULT 0,
    created_by BIGINT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_by BIGINT,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_leave_balances_user
        FOREIGN KEY (user_id)
        REFERENCES users(id),

    CONSTRAINT fk_leave_balances_created_by
        FOREIGN KEY (created_by)
        REFERENCES users(id),

    CONSTRAINT fk_leave_balances_updated_by
        FOREIGN KEY (updated_by)
        REFERENCES users(id),

    CONSTRAINT uq_leave_balances_user_year
        UNIQUE (user_id, year)
);

CREATE INDEX idx_leave_balances_user_id
    ON leave_balances(user_id);


CREATE TABLE leave_adjustments (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id BIGINT NOT NULL,
    year INTEGER NOT NULL,
    adjustment_days NUMERIC(5,2) NOT NULL,
    reason VARCHAR(500) NOT NULL,
    created_by BIGINT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_leave_adjustments_user
        FOREIGN KEY (user_id)
        REFERENCES users(id),

    CONSTRAINT fk_leave_adjustments_created_by
        FOREIGN KEY (created_by)
        REFERENCES users(id)
);

CREATE INDEX idx_leave_adjustments_user_id
    ON leave_adjustments(user_id);
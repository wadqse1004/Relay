CREATE TABLE approval_documents (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    document_no VARCHAR(50) NOT NULL UNIQUE,
    document_type_id BIGINT NOT NULL,
    requester_id BIGINT NOT NULL,
    title VARCHAR(200) NOT NULL,
    status_id BIGINT NOT NULL,
    submitted_at TIMESTAMP,
    completed_at TIMESTAMP,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_by BIGINT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_by BIGINT,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE approval_lines (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    approval_document_id BIGINT NOT NULL,
    approver_id BIGINT NOT NULL,
    sequence INTEGER NOT NULL,
    status_id BIGINT NOT NULL,
    acted_at TIMESTAMP,
    comment VARCHAR(1000),
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_by BIGINT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_by BIGINT,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT uq_approval_lines_sequence
        UNIQUE (approval_document_id, sequence)
);

CREATE TABLE approval_histories (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    approval_document_id BIGINT NOT NULL,
    approval_line_id BIGINT,
    actor_id BIGINT,
    action_id BIGINT NOT NULL,
    comment VARCHAR(1000),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

/* =========================================================
   Foreign Keys
   ========================================================= */

ALTER TABLE approval_documents
ADD CONSTRAINT fk_approval_documents_document_type
FOREIGN KEY (document_type_id)
REFERENCES common_codes(id);

ALTER TABLE approval_documents
ADD CONSTRAINT fk_approval_documents_requester
FOREIGN KEY (requester_id)
REFERENCES users(id);

ALTER TABLE approval_documents
ADD CONSTRAINT fk_approval_documents_status
FOREIGN KEY (status_id)
REFERENCES common_codes(id);

ALTER TABLE approval_documents
ADD CONSTRAINT fk_approval_documents_created_by
FOREIGN KEY (created_by)
REFERENCES users(id);

ALTER TABLE approval_documents
ADD CONSTRAINT fk_approval_documents_updated_by
FOREIGN KEY (updated_by)
REFERENCES users(id);


ALTER TABLE approval_lines
ADD CONSTRAINT fk_approval_lines_document
FOREIGN KEY (approval_document_id)
REFERENCES approval_documents(id);

ALTER TABLE approval_lines
ADD CONSTRAINT fk_approval_lines_approver
FOREIGN KEY (approver_id)
REFERENCES users(id);

ALTER TABLE approval_lines
ADD CONSTRAINT fk_approval_lines_status
FOREIGN KEY (status_id)
REFERENCES common_codes(id);

ALTER TABLE approval_lines
ADD CONSTRAINT fk_approval_lines_created_by
FOREIGN KEY (created_by)
REFERENCES users(id);

ALTER TABLE approval_lines
ADD CONSTRAINT fk_approval_lines_updated_by
FOREIGN KEY (updated_by)
REFERENCES users(id);


ALTER TABLE approval_histories
ADD CONSTRAINT fk_approval_histories_document
FOREIGN KEY (approval_document_id)
REFERENCES approval_documents(id);

ALTER TABLE approval_histories
ADD CONSTRAINT fk_approval_histories_line
FOREIGN KEY (approval_line_id)
REFERENCES approval_lines(id);

ALTER TABLE approval_histories
ADD CONSTRAINT fk_approval_histories_actor
FOREIGN KEY (actor_id)
REFERENCES users(id);

ALTER TABLE approval_histories
ADD CONSTRAINT fk_approval_histories_action
FOREIGN KEY (action_id)
REFERENCES common_codes(id);

/* =========================================================
   Indexes
   ========================================================= */

CREATE INDEX idx_approval_documents_requester
ON approval_documents(requester_id);

CREATE INDEX idx_approval_documents_status
ON approval_documents(status_id);

CREATE INDEX idx_approval_lines_document
ON approval_lines(approval_document_id);

CREATE INDEX idx_approval_lines_approver
ON approval_lines(approver_id);

CREATE INDEX idx_approval_histories_document
ON approval_histories(approval_document_id);
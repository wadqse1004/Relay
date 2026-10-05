INSERT INTO code_groups (code, name, description)
VALUES
('APPROVAL_DOCUMENT_TYPE', '결재 문서 유형', '전자결재 문서 유형'),
('APPROVAL_STATUS', '결재 상태', '결재 문서 상태'),
('APPROVAL_LINE_STATUS', '결재선 상태', '결재선 처리 상태'),
('APPROVAL_ACTION', '결재 액션', '결재 처리 이력 유형');

INSERT INTO common_codes (group_id, code, name, sort_order)
SELECT id, 'LEAVE', '연차 신청', 1
FROM code_groups
WHERE code = 'APPROVAL_DOCUMENT_TYPE';

INSERT INTO common_codes (group_id, code, name, sort_order)
SELECT id, 'DRAFT', '임시저장', 1
FROM code_groups
WHERE code = 'APPROVAL_STATUS';

INSERT INTO common_codes (group_id, code, name, sort_order)
SELECT id, 'PENDING', '결재중', 2
FROM code_groups
WHERE code = 'APPROVAL_STATUS';

INSERT INTO common_codes (group_id, code, name, sort_order)
SELECT id, 'APPROVED', '승인', 3
FROM code_groups
WHERE code = 'APPROVAL_STATUS';

INSERT INTO common_codes (group_id, code, name, sort_order)
SELECT id, 'REJECTED', '반려', 4
FROM code_groups
WHERE code = 'APPROVAL_STATUS';

INSERT INTO common_codes (group_id, code, name, sort_order)
SELECT id, 'CANCELED', '취소', 5
FROM code_groups
WHERE code = 'APPROVAL_STATUS';

INSERT INTO common_codes (group_id, code, name, sort_order)
SELECT id, 'WAITING', '대기', 1
FROM code_groups
WHERE code = 'APPROVAL_LINE_STATUS';

INSERT INTO common_codes (group_id, code, name, sort_order)
SELECT id, 'APPROVED', '승인', 2
FROM code_groups
WHERE code = 'APPROVAL_LINE_STATUS';

INSERT INTO common_codes (group_id, code, name, sort_order)
SELECT id, 'REJECTED', '반려', 3
FROM code_groups
WHERE code = 'APPROVAL_LINE_STATUS';

INSERT INTO common_codes (group_id, code, name, sort_order)
SELECT id, 'SKIPPED', '건너뜀', 4
FROM code_groups
WHERE code = 'APPROVAL_LINE_STATUS';

INSERT INTO common_codes (group_id, code, name, sort_order)
SELECT id, 'SUBMIT', '상신', 1
FROM code_groups
WHERE code = 'APPROVAL_ACTION';

INSERT INTO common_codes (group_id, code, name, sort_order)
SELECT id, 'APPROVE', '승인', 2
FROM code_groups
WHERE code = 'APPROVAL_ACTION';

INSERT INTO common_codes (group_id, code, name, sort_order)
SELECT id, 'REJECT', '반려', 3
FROM code_groups
WHERE code = 'APPROVAL_ACTION';

INSERT INTO common_codes (group_id, code, name, sort_order)
SELECT id, 'CANCEL', '취소', 4
FROM code_groups
WHERE code = 'APPROVAL_ACTION';

INSERT INTO common_codes (group_id, code, name, sort_order)
SELECT id, 'WITHDRAW', '회수', 5
FROM code_groups
WHERE code = 'APPROVAL_ACTION';
-- ============================================
-- Leave Code Group
-- ============================================

INSERT INTO code_groups (
    code,
    name,
    description,
    is_active,
    created_at,
    updated_at
)
SELECT
    'LEAVE_TYPE',
    '휴가 유형',
    '연차 및 휴가 유형',
    TRUE,
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
WHERE NOT EXISTS (
    SELECT 1
    FROM code_groups
    WHERE code = 'LEAVE_TYPE'
);


-- ============================================
-- Leave Types
-- ============================================

INSERT INTO common_codes (
    group_id,
    code,
    name,
    description,
    sort_order,
    is_active,
    created_at,
    updated_at
)
SELECT
    cg.id,
    v.code,
    v.name,
    v.description,
    v.sort_order,
    TRUE,
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
FROM code_groups cg
JOIN (
    VALUES
        ('ANNUAL',  '연차',     '1일 연차',     1),
        ('AM_HALF', '오전 반차', '오전 반차',   2),
        ('PM_HALF', '오후 반차', '오후 반차',   3),
        ('SICK',    '병가',     '병가',         4),
        ('OTHER',   '기타',     '기타 휴가',    5)
) AS v(code, name, description, sort_order)
    ON TRUE
WHERE cg.code = 'LEAVE_TYPE'
  AND NOT EXISTS (
      SELECT 1
      FROM common_codes cc
      WHERE cc.group_id = cg.id
        AND cc.code = v.code
  );
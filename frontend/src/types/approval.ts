export type ApprovalInboxItem = {
  document_id: number;
  document_no: string;
  title: string;

  requester_id: number;
  requester_name: string;

  line_id: number;
  sequence: number;

  status_code: string;
  status_name: string;

  submitted_at: string | null;

  leave_type_name?: string | null;
  start_date?: string | null;
  end_date?: string | null;
  days?: number | null;
  reason?: string | null;
};

export type ApprovalActionRequest = {
  approver_id: number;
  comment?: string;
};
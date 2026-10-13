export type LeaveBalance = {
  id: number;
  user_id: number;
  year: number;
  total_days: number;
  used_days: number;
  remaining_days: number;
};

export type LeaveRequestCreate = {
  user_id: number;
  leave_type_id: number;
  start_date: string;
  end_date: string;
  days: number;
  reason?: string;
  approver_ids: number[];
};

export type LeaveRequestResponse = {
  id: number;
  approval_document_id: number;
  user_id: number;
  leave_type_id: number;
  start_date: string;
  end_date: string;
  days: number;
  reason?: string | null;
  is_active: boolean;
  created_at: string;
};

export type LeaveRequestListItem = {
  id: number;
  approval_document_id: number;
  leave_type_id: number;
  start_date: string;
  end_date: string;
  days: number;
  reason?: string | null;
  status_code: string;
  status_name: string;
  created_at: string;
};
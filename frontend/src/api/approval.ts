import { apiClient } from "./client";

import type {
  ApprovalActionRequest,
  ApprovalInboxItem,
} from "../types/approval";

export async function getApprovalInbox(
  approverId: number
): Promise<ApprovalInboxItem[]> {
  const response = await apiClient.get<ApprovalInboxItem[]>(
    "/api/approvals/inbox",
    {
      params: {
        approver_id: approverId,
      },
    }
  );

  return response.data;
}

export async function approveDocument(
  documentId: number,
  payload: ApprovalActionRequest
) {
  const response = await apiClient.post(
    `/api/approvals/${documentId}/approve`,
    payload
  );

  return response.data;
}

export async function rejectDocument(
  documentId: number,
  payload: ApprovalActionRequest
) {
  const response = await apiClient.post(
    `/api/approvals/${documentId}/reject`,
    payload
  );

  return response.data;
}
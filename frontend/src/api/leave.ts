import { apiClient } from "./client";
import type {
  LeaveBalance,
  LeaveRequestCreate,
  LeaveRequestResponse,
  LeaveRequestListItem,
} from "../types/leave";

export async function createLeaveRequest(
  payload: LeaveRequestCreate
): Promise<LeaveRequestResponse> {
  const response = await apiClient.post<LeaveRequestResponse>(
    "/api/leaves",
    payload
  );

  return response.data;
}

export async function getLeaveBalance(
  userId: number,
  year: number
): Promise<LeaveBalance> {
  const response = await apiClient.get<LeaveBalance>(
    `/api/leaves/balance`,
    {
      params: {
        user_id: userId,
        year,
      },
    }
  );

  return response.data;
}

export async function getLeaveRequests(
  userId: number
): Promise<LeaveRequestListItem[]> {
  const response =
    await apiClient.get<LeaveRequestListItem[]>(
      "/api/leaves",
      {
        params: {
          user_id: userId,
        },
      }
    );

  return response.data;
}
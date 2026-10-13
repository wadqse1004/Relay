import { useEffect, useState, type FormEvent } from "react";

import {
  createLeaveRequest,
  getLeaveBalance,
  getLeaveRequests,
} from "../api/leave";

import type {
  LeaveBalance,
  LeaveRequestCreate,
  LeaveRequestListItem,
} from "../types/leave";

type LeaveTypeOption = {
  id: number;
  code: string;
  name: string;
};

export default function LeavePage() {
  const userId = 3;
  const year = new Date().getFullYear();

  const [balance, setBalance] = useState<LeaveBalance | null>(null);
  const [leaveRequests, setLeaveRequests] = useState<LeaveRequestListItem[]>([]);

  const [isLoading, setIsLoading] = useState(true);
  const [errorMessage, setErrorMessage] = useState("");
  const [successMessage, setSuccessMessage] = useState("");

  const [leaveTypeId, setLeaveTypeId] = useState<number>(23);
  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");
  const [days, setDays] = useState(1);
  const [reason, setReason] = useState("");

  const [approver1, setApprover1] = useState<number>(1);
  const [approver2, setApprover2] = useState<number>(2);

  const leaveTypes: LeaveTypeOption[] = [
    {
      id: 23,
      code: "ANNUAL",
      name: "연차",
    },
    {
      id: 24,
      code: "AM_HALF",
      name: "오전 반차",
    },
    {
      id: 25,
      code: "PM_HALF",
      name: "오후 반차",
    },
    {
      id: 26,
      code: "SICK",
      name: "병가",
    },
    {
      id: 27,
      code: "OTHER",
      name: "기타",
    },
  ];

  useEffect(() => {
    const loadInitialData = async () => {
      try {
        const [balanceData, requestData] = await Promise.all([
          getLeaveBalance(userId, year),
          getLeaveRequests(userId),
        ]);

        setBalance(balanceData);
        setLeaveRequests(requestData);
      } catch {
        setErrorMessage("연차 정보를 불러오지 못했습니다.");
      } finally {
        setIsLoading(false);
      }
    };

    void loadInitialData();
  }, [userId, year]);

  const handleSubmit = async (
    event: FormEvent<HTMLFormElement>
  ) => {
    event.preventDefault();

    setErrorMessage("");
    setSuccessMessage("");

    if (approver1 === approver2) {
      setErrorMessage("1차 결재자와 2차 결재자는 다르게 선택해주세요.");
      return;
    }

    try {
      const payload: LeaveRequestCreate = {
        user_id: userId,
        leave_type_id: leaveTypeId,
        start_date: startDate,
        end_date: endDate,
        days,
        reason: reason || undefined,
        approver_ids: [approver1, approver2],
      };

      await createLeaveRequest(payload);

      setSuccessMessage("연차 신청이 완료되었습니다.");

      setStartDate("");
      setEndDate("");
      setDays(1);
      setReason("");

      const [updatedBalance, updatedRequests] = await Promise.all([
        getLeaveBalance(userId, year),
        getLeaveRequests(userId),
      ]);

      setBalance(updatedBalance);
      setLeaveRequests(updatedRequests);
    } catch {
      setErrorMessage("연차 신청에 실패했습니다.");
    }
  };

  return (
    <div className="leave-page">
      <div className="leave-page-header">
        <div>
          <h1>전자결재 · 연차</h1>

          <p>
            연차 사용 현황을 확인하고 휴가를 신청할 수 있습니다.
          </p>
        </div>
      </div>

      {isLoading && (
        <div className="leave-message">
          연차 정보를 불러오는 중입니다.
        </div>
      )}

      {balance && (
        <div className="leave-balance-grid">
          <div className="leave-balance-card">
            <span>총 연차</span>
            <strong>{balance.total_days}</strong>
            <small>일</small>
          </div>

          <div className="leave-balance-card">
            <span>사용 연차</span>
            <strong>{balance.used_days}</strong>
            <small>일</small>
          </div>

          <div className="leave-balance-card">
            <span>잔여 연차</span>
            <strong>{balance.remaining_days}</strong>
            <small>일</small>
          </div>
        </div>
      )}

      <div className="leave-request-card">
        <h2>연차 신청</h2>

        <form
          className="leave-request-form"
          onSubmit={handleSubmit}
        >
          <label>
            <span>휴가 유형</span>

            <select
              value={leaveTypeId}
              onChange={(event) =>
                setLeaveTypeId(Number(event.target.value))
              }
            >
              {leaveTypes.map((type) => (
                <option
                  key={type.id}
                  value={type.id}
                >
                  {type.name}
                </option>
              ))}
            </select>
          </label>

          <div className="leave-form-row">
            <label>
              <span>시작일</span>

              <input
                type="date"
                value={startDate}
                onChange={(event) =>
                  setStartDate(event.target.value)
                }
                required
              />
            </label>

            <label>
              <span>종료일</span>

              <input
                type="date"
                value={endDate}
                onChange={(event) =>
                  setEndDate(event.target.value)
                }
                required
              />
            </label>
          </div>

          <label>
            <span>사용 일수</span>

            <input
              type="number"
              min="0.5"
              step="0.5"
              value={days}
              onChange={(event) =>
                setDays(Number(event.target.value))
              }
              required
            />
          </label>

          <label>
            <span>사유</span>

            <textarea
              value={reason}
              onChange={(event) =>
                setReason(event.target.value)
              }
              placeholder="휴가 사유를 입력하세요."
              rows={4}
            />
          </label>

          <div className="leave-form-row">
            <label>
              <span>1차 결재자</span>

              <select
                value={approver1}
                onChange={(event) =>
                  setApprover1(Number(event.target.value))
                }
              >
                <option value={1}>관리자</option>
                <option value={2}>개발자</option>
              </select>
            </label>

            <label>
              <span>2차 결재자</span>

              <select
                value={approver2}
                onChange={(event) =>
                  setApprover2(Number(event.target.value))
                }
              >
                <option value={1}>관리자</option>
                <option value={2}>개발자</option>
              </select>
            </label>
          </div>

          {errorMessage && (
            <div className="leave-error">
              {errorMessage}
            </div>
          )}

          {successMessage && (
            <div className="leave-success">
              {successMessage}
            </div>
          )}

          <button
            type="submit"
            className="leave-submit-button"
          >
            신청하기
          </button>
        </form>
      </div>

      <div className="leave-history-card">
        <h2>내 연차 신청 내역</h2>

        {leaveRequests.length === 0 ? (
          <p className="leave-empty">
            아직 신청 내역이 없습니다.
          </p>
        ) : (
          <div className="leave-history-table">
            <div className="leave-history-head">
              <span>기간</span>
              <span>일수</span>
              <span>사유</span>
              <span>상태</span>
            </div>

            {leaveRequests.map((item) => (
              <div
                className="leave-history-row"
                key={item.id}
              >
                <span>
                  {item.start_date}

                  {item.start_date !== item.end_date &&
                    ` ~ ${item.end_date}`}
                </span>

                <span>{item.days}일</span>

                <span>
                  {item.reason || "-"}
                </span>

                <span
                  className={`leave-status ${item.status_code.toLowerCase()}`}
                >
                  {item.status_name}
                </span>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
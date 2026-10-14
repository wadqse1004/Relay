import { useEffect, useState } from "react";

import {
  approveDocument,
  getApprovalInbox,
  rejectDocument,
} from "../api/approval";

import type { ApprovalInboxItem } from "../types/approval";

export default function ApprovalInboxPage() {
  const approverId = 2;

  const [items, setItems] = useState<ApprovalInboxItem[]>([]);
  const [selectedItem, setSelectedItem] =
    useState<ApprovalInboxItem | null>(null);

  const [comment, setComment] = useState("");
  const [isLoading, setIsLoading] = useState(true);

  const [errorMessage, setErrorMessage] = useState("");
  const [successMessage, setSuccessMessage] = useState("");

  useEffect(() => {
    const loadInitialInbox = async () => {
      try {
        const data = await getApprovalInbox(approverId);

        setItems(data);
      } catch {
        setErrorMessage("결재함을 불러오지 못했습니다.");
      } finally {
        setIsLoading(false);
      }
    };

    void loadInitialInbox();
  }, [approverId]);

  const refreshInbox = async () => {
    const data = await getApprovalInbox(approverId);
    setItems(data);
  };

  const handleSelectItem = (item: ApprovalInboxItem) => {
    setSelectedItem(item);
    setComment("");
    setErrorMessage("");
    setSuccessMessage("");
  };

  const handleApprove = async () => {
    if (!selectedItem) {
      return;
    }

    try {
      setErrorMessage("");
      setSuccessMessage("");

      await approveDocument(
        selectedItem.document_id,
        {
          approver_id: approverId,
          comment: comment || undefined,
        }
      );

      setSuccessMessage("승인 처리되었습니다.");

      setSelectedItem(null);
      setComment("");

      await refreshInbox();
    } catch {
      setErrorMessage("승인 처리에 실패했습니다.");
    }
  };

  const handleReject = async () => {
    if (!selectedItem) {
      return;
    }

    try {
      setErrorMessage("");
      setSuccessMessage("");

      await rejectDocument(
        selectedItem.document_id,
        {
          approver_id: approverId,
          comment: comment || undefined,
        }
      );

      setSuccessMessage("반려 처리되었습니다.");

      setSelectedItem(null);
      setComment("");

      await refreshInbox();
    } catch {
      setErrorMessage("반려 처리에 실패했습니다.");
    }
  };

  return (
    <div className="approval-inbox-page">
      <div className="approval-inbox-header">
        <div>
          <h1>결재함</h1>

          <p>
            내가 처리해야 할 결재 문서를 확인할 수 있습니다.
          </p>
        </div>
      </div>

      {isLoading && (
        <div className="approval-message">
          결재함을 불러오는 중입니다.
        </div>
      )}

      {errorMessage && (
        <div className="approval-error">
          {errorMessage}
        </div>
      )}

      {successMessage && (
        <div className="approval-success">
          {successMessage}
        </div>
      )}

      {!isLoading && items.length === 0 && (
        <div className="approval-empty">
          처리할 결재 문서가 없습니다.
        </div>
      )}

      {items.length > 0 && (
        <div className="approval-inbox-list">
          <div className="approval-inbox-head">
            <span>문서번호</span>
            <span>제목</span>
            <span>신청자</span>
            <span>결재순서</span>
            <span>상신일</span>
          </div>

          {items.map((item) => (
            <button
              key={item.line_id}
              type="button"
              className={`approval-inbox-row ${
                selectedItem?.line_id === item.line_id
                  ? "selected"
                  : ""
              }`}
              onClick={() => handleSelectItem(item)}
            >
              <span>{item.document_no}</span>

              <span>{item.title}</span>

              <span>{item.requester_name}</span>

              <span>{item.sequence}차</span>

              <span>
                {item.submitted_at
                  ? new Date(
                      item.submitted_at
                    ).toLocaleString()
                  : "-"}
              </span>
            </button>
          ))}
        </div>
      )}

      {selectedItem && (
        <div className="approval-detail-card">
          <h2>결재 처리</h2>

          <div className="approval-detail-info">
            <div>
              <span>문서번호</span>
              <strong>
                {selectedItem.document_no}
              </strong>
            </div>

            <div>
              <span>제목</span>
              <strong>
                {selectedItem.title}
              </strong>
            </div>

            <div>
              <span>신청자</span>
              <strong>
                {selectedItem.requester_name}
              </strong>
            </div>

            <div>
              <span>결재 순서</span>
              <strong>
                {selectedItem.sequence}차
              </strong>
            </div>

            <div>
              <span>결재 상태</span>
              <strong>
                {selectedItem.status_name}
              </strong>
            </div>

            <div>
              <span>상신일</span>
              <strong>
                {selectedItem.submitted_at
                  ? new Date(
                      selectedItem.submitted_at
                    ).toLocaleString()
                  : "-"}
              </strong>
            </div>

            {selectedItem.leave_type_name && (
              <>
                <div>
                  <span>휴가 유형</span>
                  <strong>
                    {selectedItem.leave_type_name}
                  </strong>
                </div>

                <div>
                  <span>사용 일수</span>
                  <strong>
                    {selectedItem.days ?? "-"}일
                  </strong>
                </div>

                <div>
                  <span>휴가 기간</span>
                  <strong>
                    {selectedItem.start_date ?? "-"}

                    {selectedItem.start_date &&
                      selectedItem.end_date &&
                      selectedItem.start_date !==
                        selectedItem.end_date &&
                      ` ~ ${selectedItem.end_date}`}
                  </strong>
                </div>

                <div>
                  <span>사유</span>
                  <strong>
                    {selectedItem.reason || "-"}
                  </strong>
                </div>
              </>
            )}
          </div>

          <label className="approval-comment">
            <span>결재 의견</span>

            <textarea
              value={comment}
              onChange={(event) =>
                setComment(event.target.value)
              }
              rows={4}
              placeholder="결재 의견을 입력하세요."
            />
          </label>

          <div className="approval-actions">
            <button
              type="button"
              className="approval-reject-button"
              onClick={handleReject}
            >
              반려
            </button>

            <button
              type="button"
              className="approval-approve-button"
              onClick={handleApprove}
            >
              승인
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
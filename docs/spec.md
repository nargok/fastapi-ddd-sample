# 概要

* **目的**: FastAPI を用いた 4 レイヤー（Presentation / Application / Domain / Infrastructure）構成の DDD 練習用サンプルを作る。
* **題材**: 勤怠管理（打刻・休憩・残業・休暇申請・月次集計）。
* **DB**: インメモリ（プロセス内のみ、永続化なし）。
* **範囲**: 単一サービス内の最小限の機能に限定。外部 ID 基盤・外部 HR システム連携は想定しない。
* **最重要ポイント**: 「ドメインモデルの明確化」「ユースケース（アプリケーションサービス）の薄さ」「レイヤー依存方向の徹底」。

---

# 非ゴール / 制約

* 本番運用の完全機能は狙わない（監査ログ/スケール/多言語対応は対象外）。
* ORM・DB 永続化は行わない（**InMemoryRepository** のみ）。
* サンプルコードの記述は不要。本書は**仕様書**のみ。
* 依存方向: Presentation → Application → Domain（← Interfaces）／Infrastructure は Domainのポートを実装。

---

# 用語と境界

* **BC（Bounded Context）**: 本サンプルでは 1 つのコンテキスト「Attendance」を定義。
* **ユーザ**: 従業員（Employee）／承認者（Approver）／管理者（Admin）はロールの違いとするが、認可は簡略化。

---

# 主要ユースケース（MVP）

1. **出勤打刻**（Clock-in）
2. **休憩開始/終了**（Start/End Break）
3. **退勤打刻**（Clock-out）
4. **勤怠日次の参照**（Get Daily Attendance）
5. **月次サマリの参照**（Get Monthly Summary）
6. **残業申請の登録/承認/却下**（Request/Approve/Reject Overtime）
7. **休暇申請の登録/承認/却下**（Request/Approve/Reject Leave）
8. **タイムシート提出/承認**（Submit/Approve Timesheet）

> まず 1〜5 を最小 MVP、6〜8 は段階導入（フェーズ2）とする。

---

# ドメインモデル

## エンティティ

* **Employee**: 従業員。属性: employeeId, name, employmentType（正社員/契約等）。
* **Timesheet**（集約ルート）: 対象月の勤怠台帳。

  * 属性: timesheetId, employeeId, yearMonth, entries（List<AttendanceEntry>）, status（Draft/Submitted/Approved/Rejected）。
* **AttendanceEntry**: 1 日分の勤怠。Timesheet 配下。

  * 属性: date, state（ClockedOut / ClockedIn / OnBreak）, clockInAt, clockOutAt, breaks（List<BreakInterval>）, notes。
* **BreakInterval**（値オブジェクト相当でも可）: 休憩区間。

  * 属性: startAt, endAt。
* **OvertimeRequest**（集約）: 残業申請。

  * 属性: requestId, employeeId, date, minutes, reason, status（Pending/Approved/Rejected）。
* **LeaveRequest**（集約）: 休暇申請。

  * 属性: requestId, employeeId, dateRange（DateRange）, type（Paid/Unpaid/Sick 等）, reason, status。

## 値オブジェクト（VO）

* **EmployeeId**, **TimesheetId**, **RequestId**: 一意識別子。
* **YearMonth**: 月次単位。
* **Date**, **DateTime**, **Minutes**（0 以上）
* **DateRange**（startDate, endDate; 前後関係チェック）
* **TimeRange**（startAt, endAt; 妥当性チェック）

## 集約・不変条件

* Timesheet は **同一 (employeeId, yearMonth)** で一意。
* AttendanceEntry は 1 日 1 レコード。状態遷移は **ClockedOut → ClockedIn → OnBreak → ClockedIn → ClockedOut** を守る。
* breaks は互いに非重複・ start < end。
* clockInAt < clockOutAt（退勤後のみ確定）。
* 月次サマリは entries 合計から算出（実労働時間 = (退勤−出勤) − 休憩合計）。

## ドメインルール（例）

* デフォルト就業規則: 9:00-18:00（休憩 60 分）※固定値で良い。
* 残業は 8 時間/日の法定内実労働超過分を minutes として扱う。
* 休暇日は打刻不可（または打刻を draft として要承認）。
* 月次は **Submitted** 状態では編集不可。**Rejected** で再編集可。

## ドメインイベント（例）

* EmployeeClockedIn(dateTime), EmployeeClockedOut(dateTime)
* BreakStarted(dateTime), BreakEnded(dateTime)
* TimesheetSubmitted(yearMonth), TimesheetApproved(yearMonth)
* OvertimeRequested/Approved/Rejected
* LeaveRequested/Approved/Rejected

---

# アプリケーション層（ユースケース）

> 入出力 DTO を受け取り、ドメインの操作をオーケストレーション。トランザクション境界はユースケース単位（InMemory なので簡略化）。

## コマンド（Write）

* **ClockInCommand**(employeeId, dateTime)
* **StartBreakCommand**(employeeId, dateTime)
* **EndBreakCommand**(employeeId, dateTime)
* **ClockOutCommand**(employeeId, dateTime)
* **SubmitTimesheetCommand**(employeeId, yearMonth)
* **ApproveTimesheetCommand**(approverId, employeeId, yearMonth)
* **RequestOvertimeCommand**(employeeId, date, minutes, reason)
* **ReviewOvertimeCommand**(approverId, requestId, approve: bool, reason?)
* **RequestLeaveCommand**(employeeId, dateRange, type, reason)
* **ReviewLeaveCommand**(approverId, requestId, approve: bool, reason?)

## クエリ（Read）

* **GetDailyAttendanceQuery**(employeeId, date)
* **GetMonthlySummaryQuery**(employeeId, yearMonth)
* **ListOvertimeRequestsQuery**(employeeId or approverId, status?)
* **ListLeaveRequestsQuery**(employeeId or approverId, status?)

## DTO（入出力の一例）

* DailyAttendanceDTO: date, state, clockInAt?, clockOutAt?, breaks[], totalWorkedMinutes
* MonthlySummaryDTO: yearMonth, totalWorkedMinutes, overtimeMinutes, days, status
* RequestDTO（Overtime/Leave 共通の要約）: id, type, date or dateRange, minutes?, reason, status

---

# プレゼンテーション層（API 仕様：エンドポイント一覧）

> FastAPI で実装。入出力は JSON。認証はモック（`X-EMPLOYEE-ID` ヘッダで従業員を識別する簡易方式）。

## v1（MVP）

* `POST /v1/attendance/clock-in` … 出勤打刻
* `POST /v1/attendance/start-break` … 休憩開始
* `POST /v1/attendance/end-break` … 休憩終了
* `POST /v1/attendance/clock-out` … 退勤打刻
* `GET  /v1/attendance/days/{date}` … 日次参照（`YYYY-MM-DD`）
* `GET  /v1/attendance/months/{yearMonth}` … 月次サマリ（`YYYY-MM`）

## v2（拡張）

* `POST /v2/timesheets/{yearMonth}/submit`
* `POST /v2/timesheets/{yearMonth}/approve`
* `POST /v2/overtime/requests`
* `POST /v2/overtime/requests/{id}/review`
* `POST /v2/leave/requests`
* `POST /v2/leave/requests/{id}/review`
* `GET  /v2/overtime/requests`
* `GET  /v2/leave/requests`

### バリデーションとエラーハンドリング（共通）

* 400: 入力不正（時刻逆転、重複休憩、状態遷移違反）
* 404: リソース未発見（Timesheet 未作成の月など）
* 409: 競合（Submitted 後の編集要求 等）
* 422: スキーマ不一致

---

# リポジトリ（ポート/アダプタ）

## Domain 側ポート（抽象）

* **TimesheetRepository**

  * `findBy(employeeId, yearMonth) -> Timesheet?`
  * `save(timesheet)`
* **OvertimeRequestRepository**

  * `findById(id)` / `save(req)` / `listByEmployee(employeeId, status?)` / `listForApprover(approverId, status?)`
* **LeaveRequestRepository**

  * 同上

## Infrastructure 側アダプタ（インメモリ）

* `InMemoryTimesheetRepository`: `Dict<(employeeId, yearMonth), Timesheet>`
* `InMemoryOvertimeRequestRepository`: `Dict<requestId, OvertimeRequest>`（索引用に `Dict<(employeeId,status), List<id>>` などは任意）
* `InMemoryLeaveRequestRepository`: 同様
* **DomainEventPublisher**（簡易 Pub/Sub）: 同期配信で OK（購読者は Application 層の通知サービス等）

---

# 状態遷移（勤怠・日次）

```
ClockedOut --clockIn--> ClockedIn --startBreak--> OnBreak --endBreak--> ClockedIn --clockOut--> ClockedOut
```

* 不正遷移例: ClockedOut から endBreak, clockOut は不可。
* 冪等性: 直近状態と同一操作は 409 を返却。

---

# 月次集計ロジック（参考仕様）

* `worked = (clockOutAt - clockInAt) - sum(breakDurations)`（分丸めは 1 分単位）
* `overtimeDaily = max(worked - 8h, 0)`
* 月次合計: `totalWorkedMinutes = Σ worked`, `overtimeMinutes = Σ overtimeDaily`

---

# プロジェクト構成（サンプル・ディレクトリ）

```
app/
  presentation/
    api/
      v1/attendance_routes.py
      v2/timesheet_routes.py
      v2/request_routes.py
    schemas/  # Pydantic DTO
    error_handlers.py
  application/
    use_cases/
      clock_in.py, start_break.py, ...
    dto/
      daily_attendance.py, monthly_summary.py, ...
    services/
      summary_service.py  # 集計ロジック調整
  domain/
    models/
      employee.py, timesheet.py, attendance_entry.py, requests.py, value_objects.py
    repositories/
      timesheet_repository.py, request_repository.py  # 抽象
    services/
      attendance_policy.py  # ルール・計算
    events/
      events.py
    exceptions.py
  infrastructure/
    repositories/
      inmem_timesheet_repo.py, inmem_request_repo.py
    messaging/
      inmem_event_publisher.py
  main.py
```

---

# テスト方針

* **Domain 単体テスト**: 不変条件・状態遷移・丸め・日跨ぎ（深夜）を中心に。
* **Application テスト**: ユースケースごとの正常/異常系。
* **API テスト**: FastAPI の TestClient で E2E 風に（最小）。
* シナリオ例:

  1. 09:00 出勤 → 12:00 休憩 → 13:00 休憩終了 → 18:00 退勤 → 実労 8h → 残業 0。
  2. 10:00 出勤 → 12:00 休憩 → 12:30 休憩終了 → 20:30 退勤 → 実労 9h → 残業 60m。
  3. 休暇申請（年休）承認済 → 当日打刻 409。
  4. 月次提出後に打刻リクエスト → 409。

---

# エラーメッセージ規約（例）

* `E1001 INVALID_STATE_TRANSITION: cannot clock-out when state is OnBreak`
* `E2001 OVERLAPPING_BREAKS`
* `E3001 ALREADY_SUBMITTED`
* `E4004 RESOURCE_NOT_FOUND`

---

# 実装ガイド（Claude Code 向けタスク分割）

1. **雛形生成**: FastAPI プロジェクト作成、`app/` 配下のディレクトリと空モジュールを作成。
2. **Domain モデル**: VO → エンティティ/集約 → 例外 → ルール（policy）→ イベントの順で作成。
3. **リポジトリ抽象**: `TimesheetRepository`, `RequestRepository` を定義。
4. **インメモリ実装**: 上記抽象の InMemory 実装とイベントパブリッシャ。
5. **ユースケース**: `clock_in`, `start_break`, `end_break`, `clock_out` から着手。DTO も定義。
6. **API ルーティング**: v1 のみ先に公開。スキーマ（Pydantic）定義。
7. **サマリ計算**: `summary_service.py` を導入し、月次集計を実装。
8. **テスト**: Domain → Application → API の順でユニットテストを追加。
9. **拡張（v2）**: 申請系（残業/休暇）とタイムシート提出/承認を追加。

---

# 入力例（フォーマットのみ・疑似）

* Clock-in: `{ "dateTime": "2025-09-28T09:00:00+09:00" }`
* Daily get: `GET /v1/attendance/days/2025-09-28`
* Monthly get: `GET /v1/attendance/months/2025-09`
  ※ これは**仕様の例示**であり、サンプルコードではない。

---

# 品質・非機能（練習用）

* ロギング: アプリ層開始/成功/失敗を INFO/ERROR で。ドメインイベント ID を含める。
* 型: MyPy 通過を目標（Optional/Union を明示）。
* ドキュメント: モジュール Docstring に役割と依存先を書く。

---

# 今後の発展案（任意）

* ポリシーの差し替え（所定労働時間・休憩規則）を Strategy として注入。
* カレンダーの祝日判定（Domain Service）。
* イベントを outbox に書き出すアダプタ（現状は in-memory）。
* 認可ガード（Role に応じて操作可否）。

---

# 受け入れ基準（MVP）

* 出勤→休憩→復帰→退勤の一連操作で月次サマリが計算される。
* 不正遷移は 400/409 を返す。
* 月次は提出後に編集不可。
* インメモリ実装のみで API が動作（サーバ再起動でデータは消える）。

---

# 付録：API スキーマ（要約）

* **Headers**: `X-EMPLOYEE-ID: <string>`
* **Date** は `YYYY-MM-DD`、**YearMonth** は `YYYY-MM`、**DateTime** は ISO 8601。
* **エンティティ識別子**は UUID 形式（文字列）。

---

> メモ：まずは **Domain が主役**。Application は薄く、Presentation はさらに薄く。Infrastructure は静かに支える——DDD のお約束でいきましょう 💪


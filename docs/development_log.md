# DevelopmentLog


## Minimum Domain Model

```
domain/models に Employee, Timesheet, AttendanceEntry, BreakInterval のクラスを実装してください。
仕様書の属性・不変条件に従い、値オブジェクトはクラスで表現してください。
まだ複雑なロジックは不要ですが、不正な値が入ったときは例外を投げるようにしてください。
```

```
 完成しました。仕様書に従って、以下のドメインモデルを実装しました：

  1. 値オブジェクト (value_objects.py):
    - ID型（EmployeeId, TimesheetId, RequestId）
    - 日付・時間型（YearMonth, Date, DateTime, Minutes, DateRange, TimeRange）
    - Enum型（EmploymentType, AttendanceState, TimesheetStatus等）
  2. BreakInterval (break_interval.py):
    - 休憩区間を表現
    - 重複チェック機能
    - 継続中/終了済みの状態管理
  3. Employee (employee.py):
    - 従業員エンティティ
    - 必須フィールドのバリデーション
  4. AttendanceEntry (attendance_entry.py):
    - 1日分の勤怠記録
    - 状態遷移（ClockedOut → ClockedIn → OnBreak → ClockedIn → ClockedOut）
    - 不正な状態遷移で例外を投げる
    - 実労働時間の計算
  5. Timesheet (timesheet.py):
    - 集約ルート
    - 月次の勤怠管理
    - ステータス管理（Draft → Submitted → Approved/Rejected）
    - 編集可能性のチェック
    - 合計労働時間・残業時間の計算

  各モデルは仕様書の不変条件を守り、不正な値が入った場合は適切な例外を投げるようになっています
```

## Repository Interface

```
domain/repositories に TimesheetRepository, OvertimeRequestRepository, LeaveRequestRepository の抽象クラスを定義してください。
仕様書のメソッドシグネチャを Python の抽象基底クラス（ABC）で表現してください。
```

```
 完成しました。仕様書に従って、以下の抽象リポジトリクラスを実装しました：

  1. TimesheetRepository (timesheet_repository.py):
    - find_by(employee_id, year_month): 従業員IDと年月でタイムシートを検索
    - save(timesheet): タイムシートを保存/更新
  2. OvertimeRequestRepository (overtime_request_repository.py):
    - find_by_id(request_id): リクエストIDで残業申請を検索
    - save(request): 残業申請を保存/更新
    - list_by_employee(employee_id, status?): 従業員IDとステータスで一覧取得
    - list_for_approver(approver_id, status?): 承認者向けの一覧取得
  3. LeaveRequestRepository (leave_request_repository.py):
    - find_by_id(request_id): リクエストIDで休暇申請を検索
    - save(request): 休暇申請を保存/更新
    - list_by_employee(employee_id, status?): 従業員IDとステータスで一覧取得
    - list_for_approver(approver_id, status?): 承認者向けの一覧取得

  また、OvertimeRequestとLeaveRequestのモデルクラスも作成し、申請の承認/却下機能を実装しました
  。すべてPythonのABC（Abstract Base Class）を使用して、抽象メソッドとして定義しています。
```
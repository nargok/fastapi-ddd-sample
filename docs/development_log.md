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


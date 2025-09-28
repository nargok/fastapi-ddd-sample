class DomainException(Exception):
    pass


class InvalidStateTransitionError(DomainException):
    pass


class OverlappingBreaksError(DomainException):
    pass


class TimesheetAlreadySubmittedError(DomainException):
    pass


class TimesheetNotFoundError(DomainException):
    pass


class InvalidTimeRangeError(DomainException):
    pass


class DuplicateEntryError(DomainException):
    pass
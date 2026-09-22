from enum import StrEnum


class State(StrEnum):
    PROPOSED = "PROPOSED"
    VALIDATING = "VALIDATING"
    BLOCKED = "BLOCKED"
    WAITING_FOR_CLARIFICATION = "WAITING_FOR_CLARIFICATION"
    WAITING_FOR_APPROVAL = "WAITING_FOR_APPROVAL"
    APPROVED = "APPROVED"
    EXECUTING = "EXECUTING"
    SUCCEEDED = "SUCCEEDED"
    FAILED = "FAILED"
    OUTCOME_UNKNOWN = "OUTCOME_UNKNOWN"
    RECOVERING = "RECOVERING"
    CANCELLED = "CANCELLED"


TRANSITIONS = {
    State.PROPOSED: {State.VALIDATING, State.CANCELLED},
    State.VALIDATING: {
        State.BLOCKED,
        State.WAITING_FOR_CLARIFICATION,
        State.WAITING_FOR_APPROVAL,
        State.APPROVED,
        State.FAILED,
    },
    State.WAITING_FOR_CLARIFICATION: {State.VALIDATING, State.CANCELLED},
    State.WAITING_FOR_APPROVAL: {State.VALIDATING, State.CANCELLED},
    State.APPROVED: {State.EXECUTING, State.CANCELLED},
    State.EXECUTING: {State.SUCCEEDED, State.FAILED, State.OUTCOME_UNKNOWN, State.BLOCKED},
    State.OUTCOME_UNKNOWN: {State.RECOVERING, State.CANCELLED},
    State.RECOVERING: {
        State.VALIDATING,
        State.SUCCEEDED,
        State.FAILED,
        State.OUTCOME_UNKNOWN,
        State.CANCELLED,
    },
}


def transition(record, target: State) -> None:
    current = State(record.state)
    if target not in TRANSITIONS.get(current, set()):
        raise ValueError(f"Invalid execution transition: {current} -> {target}")
    record.state = target.value

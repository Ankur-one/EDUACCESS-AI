from typing import Any, Optional

from app.database.models import TutorConversation


# ============================================================
# SAVE TUTOR CONVERSATION
# ============================================================

def save_tutor_conversation(
    db: Any,
    user_id: int,
    question: str,
    answer: str,
    session_id: Optional[str] = None,
) -> TutorConversation:
    """
    Save one student question and AI answer.

    session_id identifies the tutor conversation session.
    """

    question = str(question).strip()
    answer = str(answer).strip()

    if not question:

        raise ValueError(
            "Question cannot be empty."
        )

    if not answer:

        raise ValueError(
            "Answer cannot be empty."
        )

    conversation = TutorConversation(
        user_id=user_id,
        session_id=session_id,
        question=question,
        answer=answer,
    )

    db.add(conversation)

    db.commit()

    db.refresh(conversation)

    return conversation


# ============================================================
# GET USER CONVERSATIONS
# ============================================================

def get_user_conversations(
    db: Any,
    user_id: int,
    limit: Optional[int] = 50,
):
    """
    Get conversations belonging only to the logged-in user.
    """

    query = (
        db.query(TutorConversation)
        .filter(
            TutorConversation.user_id == user_id
        )
        .order_by(
            TutorConversation.created_at.asc()
        )
    )

    if limit is not None:

        query = query.limit(limit)

    return query.all()


# ============================================================
# GET SESSION CONVERSATIONS
# ============================================================

def get_session_conversations(
    db: Any,
    user_id: int,
    session_id: str,
    limit: Optional[int] = 100,
):
    """
    Get conversations belonging to one user and
    one tutor session.
    """

    query = (
        db.query(TutorConversation)
        .filter(
            TutorConversation.user_id == user_id,
            TutorConversation.session_id == session_id,
        )
        .order_by(
            TutorConversation.created_at.asc()
        )
    )

    if limit is not None:

        query = query.limit(limit)

    return query.all()


# ============================================================
# GET LATEST CONVERSATIONS
# ============================================================

def get_latest_conversations(
    db: Any,
    user_id: int,
    limit: int = 20,
):
    """
    Get the latest conversations for a user.
    """

    return (
        db.query(TutorConversation)
        .filter(
            TutorConversation.user_id == user_id
        )
        .order_by(
            TutorConversation.created_at.desc()
        )
        .limit(limit)
        .all()
    )


# ============================================================
# GET SINGLE CONVERSATION
# ============================================================

def get_tutor_conversation(
    db: Any,
    conversation_id: int,
    user_id: int,
):
    """
    Get one conversation.

    The user_id check prevents one user from
    accessing another user's conversation.
    """

    return (
        db.query(TutorConversation)
        .filter(
            TutorConversation.id == conversation_id,
            TutorConversation.user_id == user_id,
        )
        .first()
    )


# ============================================================
# DELETE ONE CONVERSATION
# ============================================================

def delete_tutor_conversation(
    db: Any,
    conversation_id: int,
    user_id: int,
) -> bool:
    """
    Delete one conversation belonging to the user.
    """

    conversation = get_tutor_conversation(
        db=db,
        conversation_id=conversation_id,
        user_id=user_id,
    )

    if conversation is None:

        return False

    db.delete(conversation)

    db.commit()

    return True


# ============================================================
# DELETE ALL USER CONVERSATIONS
# ============================================================

def delete_all_tutor_conversations(
    db: Any,
    user_id: int,
) -> int:
    """
    Delete all conversations belonging to one user.

    Returns:
        Number of deleted conversations.
    """

    conversations = (
        db.query(TutorConversation)
        .filter(
            TutorConversation.user_id == user_id
        )
        .all()
    )

    count = len(conversations)

    for conversation in conversations:

        db.delete(conversation)

    db.commit()

    return count


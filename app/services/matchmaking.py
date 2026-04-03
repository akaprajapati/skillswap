from sqlalchemy.orm import Session
from app.models.user import User
from app.models.match import Swipe, Match


def check_skill_match(user1: User, user2: User):
    # 🎯 Core Logic:
    # user1 offered matches user2 wanted
    # AND user2 offered matches user1 wanted

    user1_offered = {s.id for s in user1.offered_skills}
    user1_wanted = {s.id for s in user1.wanted_skills}

    user2_offered = {s.id for s in user2.offered_skills}
    user2_wanted = {s.id for s in user2.wanted_skills}

    condition1 = user1_offered & user2_wanted
    condition2 = user2_offered & user1_wanted

    return bool(condition1 and condition2)


def create_swipe(db: Session, from_user: int, to_user: int, action: str):
    swipe = Swipe(
        from_user_id=from_user,
        to_user_id=to_user,
        action=action
    )
    db.add(swipe)
    db.commit()

    return swipe


def check_mutual_like(db: Session, user1: int, user2: int):
    swipe = db.query(Swipe).filter_by(
        from_user_id=user2,
        to_user_id=user1,
        action="like"
    ).first()

    return swipe is not None


def create_match(db: Session, user1: int, user2: int):
    existing = db.query(Match).filter(
        ((Match.user1_id == user1) & (Match.user2_id == user2)) |
        ((Match.user1_id == user2) & (Match.user2_id == user1))
    ).first()

    if existing:
        return existing

    match = Match(user1_id=user1, user2_id=user2)
    db.add(match)
    db.commit()

    return match
from datetime import datetime

from app.models import Study, User


async def create_study_in_db(title, content, owner: User, max_participants: int, expire_time: datetime):
    """Create Study"""
    study = Study(title=title, content=content, owner=owner, max_participants=max_participants, expire_time=expire_time)

    await study.create()

    return study


async def get_study_paginate(page: int, limit: int):
    start_idx = (page - 1) * limit
    content = await Study.find().limit(limit).skip(start_idx).to_list()

    return content


async def get_study_by_id(study_id: str):
    content = await Study.get(study_id)

    return content


async def get_owner_from_study(study: Study):
    await study.fetch_link(Study.owner)

    return study.owner


async def is_participants_left(study: Study):
    return study.cur_participants < study.max_participants


async def move_waiter_to_participants(study: Study, user: User):
    study.participants_wait.remove(user)
    study.participants.append(user)
    study.cur_participants = len(study.participants)
    await study.replace()
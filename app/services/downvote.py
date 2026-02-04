from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.downvote import DownvoteCreate, DownvoteCreateResponse
from app.models.downvote import Downvote
from app.services import post as post_service
from app.services import comment as comment_service


# Get by user id and post id
async def get_by_user_id_and_post_id(user_id: UUID, post_id: UUID, db: AsyncSession):
    result = await db.execute(
        select(Downvote).where(
            (Downvote.user_id == user_id) & (Downvote.post_id == post_id)
        )
    )

    return result.scalars().first()


# Get by user id and comment id
async def get_by_user_id_and_comment_id(
    user_id: UUID, comment_id: UUID, db: AsyncSession
):
    result = await db.execute(
        select(Downvote).where(
            (Downvote.user_id == user_id) & (Downvote.comment_id == comment_id)
        )
    )

    return result.scalars().first()


# Create
async def create(payload: DownvoteCreate, db: AsyncSession):
    new_downvote = Downvote(
        post_id=payload.post_id,
        comment_id=payload.comment_id,
        user_id=payload.user_id,
    )

    db.add(new_downvote)
    await db.commit()
    await db.refresh(new_downvote)
    return new_downvote


# Delete
async def delete(downvote: Downvote, db: AsyncSession):
    await db.delete(downvote)
    await db.commit()


# Toggle
async def toggle(
    payload: DownvoteCreate, db: AsyncSession
) -> DownvoteCreateResponse | None:
    if payload.post_id:
        await post_service.get_by_id(id=payload.post_id, db=db)

        downvote = await get_by_user_id_and_post_id(
            user_id=payload.user_id, post_id=payload.post_id, db=db
        )

        if not downvote:
            return await create(payload=payload, db=db)
        else:
            await delete(downvote=downvote, db=db)
            return None
    else:
        await comment_service.get_by_id(id=payload.comment_id, db=db)

        downvote = await get_by_user_id_and_comment_id(
            user_id=payload.user_id, comment_id=payload.comment_id, db=db
        )

        if not downvote:
            return await create(payload=payload, db=db)
        else:
            await delete(downvote=downvote, db=db)
            return None

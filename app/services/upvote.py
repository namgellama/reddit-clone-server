from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.upvote import UpvoteCreate, UpvoteCreateResponse
from app.models.upvote import Upvote
from app.services import post as post_service
from app.services import comment as comment_service
from app.services import downvote as downvote_service


# Get by user id and post id
async def get_by_user_id_and_post_id(user_id: UUID, post_id: UUID, db: AsyncSession):
    result = await db.execute(
        select(Upvote).where((Upvote.user_id == user_id) & (Upvote.post_id == post_id))
    )

    return result.scalars().first()


# Get by user id and comment id
async def get_by_user_id_and_comment_id(
    user_id: UUID, comment_id: UUID, db: AsyncSession
):
    result = await db.execute(
        select(Upvote).where(
            (Upvote.user_id == user_id) & (Upvote.comment_id == comment_id)
        )
    )

    return result.scalars().first()


# Create
async def create(payload: UpvoteCreate, db: AsyncSession):
    new_upvote = Upvote(
        post_id=payload.post_id,
        comment_id=payload.comment_id,
        user_id=payload.user_id,
    )

    db.add(new_upvote)
    await db.commit()
    await db.refresh(new_upvote)
    return new_upvote


# Delete
async def delete(upvote: Upvote, db: AsyncSession):
    await db.delete(upvote)
    await db.commit()


# Toggle
async def toggle(
    payload: UpvoteCreate, db: AsyncSession
) -> UpvoteCreateResponse | None:
    if payload.post_id:
        await post_service.get_by_id(id=payload.post_id, db=db)

        upvote = await get_by_user_id_and_post_id(
            user_id=payload.user_id, post_id=payload.post_id, db=db
        )

        if not upvote:
            new_upvote = await create(payload=payload, db=db)
            downvote = await downvote_service.get_by_user_id_and_post_id(
                user_id=payload.user_id, post_id=payload.post_id, db=db
            )

            if downvote:
                await downvote_service.delete(downvote=downvote, db=db)

            return new_upvote
        else:
            await delete(upvote=upvote, db=db)
            return None
    else:
        await comment_service.get_by_id(id=payload.comment_id, db=db)

        upvote = await get_by_user_id_and_comment_id(
            user_id=payload.user_id, comment_id=payload.comment_id, db=db
        )

        if not upvote:
            new_upvote = await create(payload=payload, db=db)
            downvote = await downvote_service.get_by_user_id_and_comment_id(
                user_id=payload.user_id, comment_id=payload.comment_id, db=db
            )

            if downvote:
                await downvote_service.delete(downvote=downvote, db=db)

            return new_upvote
        else:
            await delete(upvote=upvote, db=db)
            return None

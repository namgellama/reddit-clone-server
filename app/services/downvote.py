from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.downvote import Downvote
from app.services import post as post_service
from app.services import comment as comment_service
from app.services import upvote as upvote_service


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


# Delete
async def delete(downvote: Downvote, db: AsyncSession):
    await db.delete(downvote)
    await db.commit()


# Toggle post downvote
async def toggle_post_downvote(post_id: UUID, user_id: UUID, db: AsyncSession):
    # Check if post exists
    await post_service.fetch_by_id(id=post_id, db=db)

    # Check if downvote by the current user exists
    downvote = await get_by_user_id_and_post_id(user_id=user_id, post_id=post_id, db=db)

    if not downvote:
        # Create new downvote
        new_downvote = Downvote(
            post_id=post_id,
            comment_id=None,
            user_id=user_id,
        )

        db.add(new_downvote)
        await db.commit()
        await db.refresh(new_downvote)

        # Check if there is upvote in that post done by the current user
        upvote = await upvote_service.get_by_user_id_and_post_id(
            user_id=user_id, post_id=post_id, db=db
        )

        if upvote:
            # Delete upvote if exists
            await upvote_service.delete(upvote=upvote, db=db)

        return new_downvote
    else:
        # Delete downvote if already exists to have toggle effect
        await delete(downvote=downvote, db=db)
        return None


# Toggle comment downvote
async def toggle_comment_downvote(
    post_id: UUID, comment_id: UUID, user_id: UUID, db: AsyncSession
):
    # Check if comment exists
    await comment_service.get_by_post_id_and_comment_id(post_id, comment_id, db)

    # Check if downvote by the current user exists
    downvote = await get_by_user_id_and_comment_id(
        user_id=user_id, comment_id=comment_id, db=db
    )

    if not downvote:
        # Create new downvote
        new_downvote = Downvote(
            post_id=None,
            comment_id=comment_id,
            user_id=user_id,
        )

        db.add(new_downvote)
        await db.commit()
        await db.refresh(new_downvote)

        # Check if there is upvote in that post done by the current user
        upvote = await upvote_service.get_by_user_id_and_comment_id(
            user_id=user_id, comment_id=comment_id, db=db
        )

        if upvote:
            # Delete upvote if exists
            await upvote_service.delete(upvote=upvote, db=db)

        return new_downvote
    else:
        # Delete downvote if already exists to have toggle effect
        await delete(downvote=downvote, db=db)
        return None

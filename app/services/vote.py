from uuid import UUID
from sqlalchemy import select, func, case
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.vote import Vote, VoteType
from app.schemas.vote import VoteRequest, VoteResponse
from app.services import post as post_service
from app.services import comment as comment_service


# Get by user id and post id
async def get_by_user_id_and_post_id(user_id: UUID, post_id: UUID, db: AsyncSession):
    result = await db.execute(
        select(Vote).where((Vote.user_id == user_id) & (Vote.post_id == post_id))
    )

    return result.scalars().first()


# Get by user id and comment id
async def get_by_user_id_and_comment_id(
    user_id: UUID, comment_id: UUID, db: AsyncSession
):
    result = await db.execute(
        select(Vote).where((Vote.user_id == user_id) & (Vote.comment_id == comment_id))
    )

    return result.scalars().first()


# Delete
async def delete(vote: Vote, db: AsyncSession):
    await db.delete(vote)
    await db.commit()


# Toggle post vote
async def toggle_post_vote(
    post_id: UUID, body: VoteRequest, user_id: UUID, db: AsyncSession
):
    # Check if post exists
    await post_service.fetch_by_id(id=post_id, db=db)

    # Check if vote by the current user exists
    vote = await get_by_user_id_and_post_id(user_id=user_id, post_id=post_id, db=db)

    vote_type = None

    if vote:
        # If vote exists and vote type is same as body type, delete the vote
        if vote.type == body.type:
            await delete(vote=vote, db=db)
        else:
            # Else update the vote type
            vote.type = body.type

            await db.commit()
            await db.refresh(vote)

            vote_type = vote.type
    else:
        # If vote doesn't exist, create new vote
        new_vote = Vote(
            type=body.type,
            post_id=post_id,
            comment_id=None,
            user_id=user_id,
        )

        db.add(new_vote)
        await db.commit()
        await db.refresh(new_vote)

        vote_type = new_vote.type

    # Score calculation
    stmt = select(
        func.coalesce(
            func.sum(
                case(
                    (Vote.type == VoteType.UPVOTE, 1),
                    (Vote.type == VoteType.DOWNVOTE, -1),
                    else_=0,
                )
            ),
            0,
        )
    ).where(Vote.post_id == post_id)

    result = await db.execute(stmt)
    score = result.scalar()

    return VoteResponse(
        vote_type=vote_type,
        score=score,
    )


# Toggle comment vote
async def toggle_comment_vote(
    post_id: UUID, comment_id: UUID, body: VoteRequest, user_id: UUID, db: AsyncSession
):
    # Check if post and comment exists
    await comment_service.get_by_post_id_and_comment_id(
        post_id=post_id, comment_id=comment_id, db=db
    )

    # Check if vote by the current user exists
    vote = await get_by_user_id_and_comment_id(
        user_id=user_id, comment_id=comment_id, db=db
    )

    vote_type = None

    if vote:
        # If vote exists and vote type is same as body type, delete the vote
        if vote.type == body.type:
            await delete(vote=vote, db=db)
        else:
            # Else update the vote type
            vote.type = body.type

            await db.commit()
            await db.refresh(vote)

            vote_type = vote.type
    else:
        # If vote doesn't exist, create new vote
        new_vote = Vote(
            type=body.type,
            post_id=None,
            comment_id=comment_id,
            user_id=user_id,
        )

        db.add(new_vote)
        await db.commit()
        await db.refresh(new_vote)

        vote_type = new_vote.type

    # Score calculation
    stmt = select(
        func.coalesce(
            func.sum(
                case(
                    (Vote.type == VoteType.UPVOTE, 1),
                    (Vote.type == VoteType.DOWNVOTE, -1),
                    else_=0,
                )
            ),
            0,
        )
    ).where(Vote.comment_id == comment_id)

    result = await db.execute(stmt)
    score = result.scalar()

    return VoteResponse(
        vote_type=vote_type,
        score=score,
    )

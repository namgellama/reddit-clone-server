from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy import select, func, distinct, case
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.post import Post
from app.models.comment import Comment
from app.models.vote import Vote, VoteType
from app.schemas.post import PostCreate, PostUpdate
from app.services.image import ImageService


# Get user vote case
def get_user_vote_case(user_id: UUID | None):
    if user_id is not None:
        return case(
            (
                Vote.user_id == user_id,
                case(
                    (Vote.type == VoteType.UPVOTE, 1),
                    (Vote.type == VoteType.DOWNVOTE, -1),
                    else_=0,
                ),
            ),
        )

    return 0


# Get all
async def get_all(user_id: UUID | None, db: AsyncSession):

    stmt = (
        select(
            Post,
            func.count(distinct(Comment.id)).label("comment_count"),
            func.coalesce(
                func.sum(
                    case(
                        (Vote.type == VoteType.UPVOTE, 1),
                        (Vote.type == VoteType.DOWNVOTE, -1),
                        else_=0,
                    )
                ),
                0,
            ).label("score"),
            func.max(get_user_vote_case(user_id=user_id)).label("user_vote"),
        )
        # User vote (0 = none, 1 = upvote, -1 = downvote)
        .outerjoin(Comment, Comment.post_id == Post.id)
        .outerjoin(Vote, Vote.post_id == Post.id)
        .options(selectinload(Post.user))
        .group_by(Post.id)
        .order_by(Post.date_posted.desc())
    )

    result = await db.execute(stmt)
    rows: list[tuple[Post, int, int, int]] = result.all()

    posts = []

    for post, comment_count, score, user_vote in rows:
        posts.append(
            {
                "id": post.id,
                "title": post.title,
                "content": post.content,
                "images": post.images,
                "date_posted": post.date_posted,
                "user": {
                    "id": post.user.id,
                    "username": post.user.username,
                    "email": post.user.email,
                },
                "score": score,
                "user_vote": (
                    "UPVOTE"
                    if user_vote == 1
                    else "DOWNVOTE" if user_vote == -1 else None
                ),
                "comment_count": comment_count,
            }
        )

    return posts


# Fetch by id
async def fetch_by_id(id: UUID, db: AsyncSession):
    result = await db.execute(select(Post).where(Post.id == id))
    post = result.scalars().first()

    if not post:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Post not found")

    return post


# Get by id
async def get_by_id(id: UUID, user_id: UUID | None, db: AsyncSession):
    stmt = (
        select(
            Post,
            func.count(Comment.id).label("comment_count"),
            func.coalesce(
                func.sum(
                    case(
                        (Vote.type == VoteType.UPVOTE, 1),
                        (Vote.type == VoteType.DOWNVOTE, -1),
                        else_=0,
                    )
                ),
                0,
            ).label("score"),
            func.max(get_user_vote_case(user_id=user_id)).label("user_vote"),
        )
        # User vote (0 = none, 1 = upvote, -1 = downvote)
        .outerjoin(Comment, Comment.post_id == Post.id)
        .outerjoin(Vote, Vote.post_id == Post.id)
        .options(selectinload(Post.user))
        .where(Post.id == id)
        .group_by(Post.id)
    )

    result = await db.execute(stmt)
    row: tuple[Post, int, int, int] = result.first()

    if not row:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Post not found")

    post, comment_count, score, user_vote = row

    return {
        "id": post.id,
        "title": post.title,
        "content": post.content,
        "images": post.images,
        "date_posted": post.date_posted,
        "user": {
            "id": post.user.id,
            "username": post.user.username,
            "email": post.user.email,
        },
        "score": score,
        "user_vote": (
            "UPVOTE" if user_vote == 1 else "DOWNVOTE" if user_vote == -1 else None
        ),
        "comment_count": comment_count,
    }


# Create
async def create(payload: PostCreate, db: AsyncSession):
    new_post = Post(
        title=payload.title,
        content=payload.content,
        images=payload.images,
        user_id=payload.user_id,
    )

    db.add(new_post)
    await db.commit()
    await db.refresh(new_post, attribute_names=["author"])

    return new_post


# Update
async def update(payload: PostUpdate, db: AsyncSession):
    post = await fetch_by_id(id=payload.id, db=db)

    if post.user_id != payload.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not allowed")

    old_images = post.images or []
    previous_images = payload.previous_images or []
    new_images = payload.images or []

    if payload.title is not None:
        post.title = payload.title

    if payload.content is not None:
        post.content = payload.content

    if payload.images is not None or payload.previous_images is not None:
        post.images = previous_images + new_images

    await db.commit()
    await db.refresh(post, attribute_names=["author"])

    if len(previous_images) > 0:
        for image in old_images:
            if image not in previous_images:
                ImageService.delete_image(image)
    else:
        for image in old_images:
            ImageService.delete_image(image)

    return post


# Delete
async def delete(id: UUID, user_id: UUID, db: AsyncSession):
    post = await get_by_id(id=id, db=db)

    if post.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not allowed")

    await db.delete(post)
    await db.commit()

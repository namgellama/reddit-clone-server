import { prisma } from '@/shared/lib/prisma';
import commentService from '../comment/comment.service';
import postService from '../post/post.service';
import { IToggleUpvoteInput } from './upvote.validation';

const upvoteService = {
    // Toggle
    toggle: async (body: IToggleUpvoteInput, userId: string) => {
        const { entityType, entityId } = body;

        if (entityType === 'post') {
            await postService.getById(entityId);

            const existingUpvote = await upvoteService.getById(
                entityId,
                entityType,
                userId
            );

            if (existingUpvote) {
                await upvoteService.delete(entityId, entityType, userId);

                return { postId: entityId, upvoted: false };
            }

            await upvoteService.create(entityId, entityType, userId);

            return { postId: entityId, upvoted: true };
        }

        await commentService.getById(entityId);

        const existingUpvote = await upvoteService.getById(
            entityId,
            entityType,
            userId
        );

        if (existingUpvote) {
            await upvoteService.delete(entityId, entityType, userId);

            return { commentId: entityId, upvoted: false };
        }

        await upvoteService.create(entityId, entityType, userId);

        return { commentId: entityId, upvoted: true };
    },

    // Create
    create: async (
        entityId: string,
        entityType: 'post' | 'comment',
        userId: string
    ) => {
        if (entityType === 'post')
            return await prisma.upvote.create({
                data: {
                    postId: entityId,
                    userId,
                },
            });

        return await prisma.upvote.create({
            data: {
                commentId: entityId,
                userId,
            },
        });
    },

    // Get by id
    getById: async (
        entityId: string,
        entityType: 'post' | 'comment',
        userId: string
    ) => {
        if (entityType === 'post') {
            return await prisma.upvote.findUnique({
                where: {
                    userId_postId: {
                        userId,
                        postId: entityId,
                    },
                },
            });
        } else {
            return await prisma.upvote.findUnique({
                where: {
                    userId_commentId: {
                        userId,
                        commentId: entityId,
                    },
                },
            });
        }
    },

    // Delete
    delete: async (
        entityId: string,
        entityType: 'post' | 'comment',
        userId: string
    ) => {
        if (entityType === 'post')
            return await prisma.upvote.delete({
                where: {
                    userId_postId: {
                        userId,
                        postId: entityId,
                    },
                },
            });

        return await prisma.upvote.delete({
            where: {
                userId_commentId: {
                    userId,
                    commentId: entityId,
                },
            },
        });
    },
};

export default upvoteService;

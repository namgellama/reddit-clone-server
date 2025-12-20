import { prisma } from '@/shared/lib/prisma';
import commentService from '../comment/comment.service';
import postService from '../post/post.service';
import { IToggleDownvoteInput } from './downvote.validation';

const downvoteService = {
    // Toggle
    toggle: async (body: IToggleDownvoteInput, userId: string) => {
        const { entityType, entityId } = body;

        if (entityType === 'post') {
            await postService.getById(entityId);

            const existingDownvote = await downvoteService.getById(
                entityId,
                entityType,
                userId
            );

            if (existingDownvote) {
                await downvoteService.delete(entityId, entityType, userId);

                return { postId: entityId, downvoted: false };
            }

            await downvoteService.create(entityId, entityType, userId);

            return { postId: entityId, downvoted: true };
        }

        await commentService.getById(entityId);

        const existingDownvote = await downvoteService.getById(
            entityId,
            entityType,
            userId
        );

        if (existingDownvote) {
            await downvoteService.delete(entityId, entityType, userId);

            return { commentId: entityId, downvoted: false };
        }

        await downvoteService.create(entityId, entityType, userId);

        return { commentId: entityId, downvoted: true };
    },

    // Create
    create: async (
        entityId: string,
        entityType: 'post' | 'comment',
        userId: string
    ) => {
        if (entityType === 'post')
            return await prisma.downvote.create({
                data: {
                    postId: entityId,
                    userId,
                },
            });

        return await prisma.downvote.create({
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
            return await prisma.downvote.findUnique({
                where: {
                    userId_postId: {
                        userId,
                        postId: entityId,
                    },
                },
            });
        } else {
            return await prisma.downvote.findUnique({
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
            return await prisma.downvote.delete({
                where: {
                    userId_postId: {
                        userId,
                        postId: entityId,
                    },
                },
            });

        return await prisma.downvote.delete({
            where: {
                userId_commentId: {
                    userId,
                    commentId: entityId,
                },
            },
        });
    },
};

export default downvoteService;

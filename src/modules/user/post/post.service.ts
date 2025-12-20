import { StatusCodes } from 'http-status-codes';

import { prisma } from '@/shared/lib/prisma';
import { ensureOwner } from '@/shared/utils/ensure-owner.utils';
import { apiError } from '@/shared/utils/error.utils';
import { ICreatePostInput } from './post.validations';

const postService = {
    // Create
    create: async (body: ICreatePostInput, userId: string) => {
        return await prisma.post.create({
            data: {
                ...body,
                userId,
            },
        });
    },

    // Get all
    getAll: async () => {
        const posts = await prisma.post.findMany({
            include: {
                _count: {
                    select: {
                        comments: true,
                        upvotes: true,
                    },
                },
            },
        });

        return posts.map(({ _count, ...rest }) => ({
            ...rest,
            commentsCount: _count.comments,
            upvotesCount: _count.upvotes,
        }));
    },

    // Get by id
    getById: async (id: string) => {
        const existingPost = await prisma.post.findUnique({
            where: { id },
            include: {
                comments: {
                    include: {
                        _count: {
                            select: {
                                replies: true,
                                upvotes: true,
                            },
                        },
                    },
                },
                _count: {
                    select: {
                        comments: true,
                        upvotes: true,
                    },
                },
            },
        });

        if (!existingPost)
            throw apiError(StatusCodes.NOT_FOUND, 'Post not found');

        const { _count, comments, ...rest } = existingPost;

        return {
            ...rest,
            comments: comments.map(({ _count, ...rest }) => ({
                ...rest,
                repliesCount: _count.replies,
                upvotesCount: _count.upvotes,
            })),
            commentsCount: _count.comments,
            upvotesCount: _count.upvotes,
        };
    },

    // Update
    update: async (id: string, body: ICreatePostInput, userId: string) => {
        const existingPost = await postService.getById(id);
        ensureOwner(existingPost.userId, userId);

        return await prisma.post.update({ where: { id, userId }, data: body });
    },

    // Delete
    delete: async (id: string, userId: string) => {
        const existingPost = await postService.getById(id);
        ensureOwner(existingPost.id, userId);

        await prisma.post.delete({ where: { id } });
    },
};

export default postService;

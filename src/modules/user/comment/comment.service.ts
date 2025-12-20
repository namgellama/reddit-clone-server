import { StatusCodes } from 'http-status-codes';

import { prisma } from '@/shared/lib/prisma';
import { ensureOwner } from '@/shared/utils/ensure-owner.utils';
import { ApiError, apiError } from '@/shared/utils/error.utils';
import postService from '../post/post.service';
import { ICreateCommentInput } from './comment.validation';

const commentService = {
    // Create
    create: async (
        body: ICreateCommentInput,
        postId: string,
        userId: string
    ) => {
        await postService.getById(postId);

        return await prisma.comment.create({
            data: {
                ...body,
                postId,
                userId,
            },
        });
    },

    // Reply
    reply: async (
        body: ICreateCommentInput,
        postId: string,
        commentId: string,
        userId: string
    ) => {
        await postService.getById(postId);

        const existingComment = await commentService.getById(postId, commentId);

        if (existingComment.parentId)
            throw new ApiError(
                'Comment depth exceeded',
                StatusCodes.BAD_REQUEST
            );

        return await prisma.comment.create({
            data: {
                ...body,
                postId,
                parentId: commentId,
                userId,
            },
        });
    },

    // Get all
    getAll: async (postId: string) => {
        await postService.getById(postId);

        return await prisma.comment.findMany({ where: { postId } });
    },

    // Get all
    getAllReplies: async (postId: string, commentId: string) => {
        await postService.getById(postId);

        await commentService.getById(postId, commentId);

        return await prisma.comment.findMany({
            where: { postId, parentId: commentId },
        });
    },

    // Get by id
    getById: async (postId: string, commentId: string) => {
        const existingComment = await prisma.comment.findUnique({
            where: { id: commentId, postId },
        });

        if (!existingComment)
            throw apiError(StatusCodes.NOT_FOUND, 'Comment not found');

        return existingComment;
    },

    // Update
    update: async (
        body: ICreateCommentInput,
        postId: string,
        commentId: string,
        userId: string
    ) => {
        const existingComment = await commentService.getById(postId, commentId);

        ensureOwner(existingComment.userId, userId);

        return await prisma.comment.update({
            where: { id: commentId, postId },
            data: body,
        });
    },

    // Delete
    delete: async (postId: string, commentId: string, userId: string) => {
        const existingComment = await commentService.getById(postId, commentId);

        ensureOwner(existingComment.userId, userId);

        await prisma.comment.delete({ where: { id: commentId, postId } });
    },
};

export default commentService;

import { prisma } from '@/shared/lib/prisma';
import postService from '../post/post.service';
import { ICreateCommentInput } from './comment.validation';
import { ApiError, apiError } from '@/shared/utils/error.utils';
import { StatusCodes } from 'http-status-codes';

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

        const existingComment = await commentService.getById(commentId);

        if (existingComment.postId !== postId)
            throw new ApiError(
                'Comment does not belong to this post',
                StatusCodes.BAD_REQUEST
            );

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

        const existingComment = await commentService.getById(commentId);

        if (existingComment.postId !== postId)
            throw new ApiError(
                'Comment does not belong to this post',
                StatusCodes.BAD_REQUEST
            );

        return await prisma.comment.findMany({
            where: { postId, parentId: commentId },
        });
    },

    // Get by id
    getById: async (id: string) => {
        const existingComment = await prisma.comment.findUnique({
            where: { id },
        });

        if (!existingComment)
            throw apiError(StatusCodes.NOT_FOUND, 'Comment not found');

        return existingComment;
    },
};

export default commentService;

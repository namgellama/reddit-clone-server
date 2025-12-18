import { NextFunction, Request, Response } from 'express';

import commentService from './comment.service';
import { ICreateCommentInput } from './comment.validation';
import { sendResponse } from '@/shared/utils/response.utils';
import { StatusCodes } from 'http-status-codes';

const commentController = {
    // Create comment
    create: async (
        req: Request<{ postId: string }, {}, ICreateCommentInput>,
        res: Response,
        next: NextFunction
    ) => {
        try {
            const { postId } = req.params;
            const body = req.body;
            const userId = req.user?.id!;

            const newComment = await commentService.create(
                body,
                postId,
                userId
            );

            sendResponse(
                res,
                'Comment created successfully',
                newComment,
                StatusCodes.CREATED
            );
        } catch (error) {
            next(error);
        }
    },

    // Reply comment
    reply: async (
        req: Request<
            { postId: string; commentId: string },
            {},
            ICreateCommentInput
        >,
        res: Response,
        next: NextFunction
    ) => {
        try {
            const { postId, commentId } = req.params;
            const body = req.body;
            const userId = req.user?.id!;

            const newReply = await commentService.reply(
                body,
                postId,
                commentId,
                userId
            );

            sendResponse(
                res,
                'Reply created successfully',
                newReply,
                StatusCodes.CREATED
            );
        } catch (error) {
            next(error);
        }
    },

    // Get all comments
    getAll: async (
        req: Request<{ postId: string }>,
        res: Response,
        next: NextFunction
    ) => {
        try {
            const { postId } = req.params;

            const comments = await commentService.getAll(postId);

            sendResponse(res, 'Comments fetched successfully', comments);
        } catch (error) {
            next(error);
        }
    },

    // Get all comments replies
    getAllReplies: async (
        req: Request<{ postId: string; commentId: string }>,
        res: Response,
        next: NextFunction
    ) => {
        try {
            const { postId, commentId } = req.params;

            const comments = await commentService.getAllReplies(
                postId,
                commentId
            );

            sendResponse(res, 'Comment replies fetched successfully', comments);
        } catch (error) {
            next(error);
        }
    },
};

export default commentController;

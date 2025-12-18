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
};

export default commentController;

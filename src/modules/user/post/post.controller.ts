import { NextFunction, Request, Response } from 'express';

import { sendResponse } from '@/shared/utils/response.utils';
import userPostService from './post.service';
import { ICreatePostInput } from './post.validations';
import { StatusCodes } from 'http-status-codes';

const userPostController = {
    // Create post
    create: async (
        req: Request<{}, {}, ICreatePostInput>,
        res: Response,
        next: NextFunction
    ) => {
        try {
            const newPost = await userPostService.create(req.body);

            sendResponse(
                res,
                'Post created successfully',
                newPost,
                StatusCodes.CREATED
            );
        } catch (error) {
            next(error);
        }
    },

    // Get all posts
    getAll: async (req: Request, res: Response, next: NextFunction) => {
        try {
            const posts = await userPostService.getAll();

            sendResponse(res, 'Posts fetched successfully', posts);
        } catch (error) {
            next(error);
        }
    },

    // Get post by id
    getById: async (
        req: Request<{ id: string }>,
        res: Response,
        next: NextFunction
    ) => {
        try {
            const { id } = req.params;

            const post = await userPostService.getById(id);

            sendResponse(res, 'Post fetched successfully', post);
        } catch (error) {
            next(error);
        }
    },

    // Update post
    update: async (
        req: Request<{ id: string }, {}, ICreatePostInput>,
        res: Response,
        next: NextFunction
    ) => {
        try {
            const { id } = req.params;
            const body = req.body;

            const post = await userPostService.update(id, body);

            sendResponse(res, 'Post updated successfully', post);
        } catch (error) {
            next(error);
        }
    },

    // Delete post
    delete: async (
        req: Request<{ id: string }>,
        res: Response,
        next: NextFunction
    ) => {
        try {
            const { id } = req.params;

            await userPostService.delete(id);

            sendResponse(
                res,
                'Post deleted successfully',
                {},
                StatusCodes.NO_CONTENT
            );
        } catch (error) {
            next(error);
        }
    },
};

export default userPostController;

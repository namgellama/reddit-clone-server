import { NextFunction, Request, Response } from 'express';

import { sendResponse } from '@/utils/response.utils';
import userPostService from './post.service';
import { ICreatePostInput } from './post.validations';

const userPostController = {
    // Create post
    create: async (
        req: Request<{}, {}, ICreatePostInput>,
        res: Response,
        next: NextFunction
    ) => {
        try {
            const newPost = await userPostService.create(req.body);

            sendResponse(res, 'Post created successfully', newPost);
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
};

export default userPostController;

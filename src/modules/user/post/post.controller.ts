import { NextFunction, Request, Response } from 'express';

import { sendResponse } from '@/shared/utils/response.utils';
import { StatusCodes } from 'http-status-codes';
import postService from './post.service';
import { ICreatePostInput } from './post.validations';

const postController = {
    // Create post
    create: async (
        req: Request<{}, {}, ICreatePostInput>,
        res: Response,
        next: NextFunction
    ) => {
        try {
            const userId = req.user?.id!;

            const files = req.files as Express.Multer.File[] | undefined;

            const body: ICreatePostInput & { images?: Express.Multer.File[] } =
                {
                    ...req.body,
                    images: files,
                };

            const newPost = await postService.create(body, userId);

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
            const posts = await postService.getAll();

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

            const post = await postService.getById(id);

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
            const userId = req.user?.id!;

            const post = await postService.update(id, body, userId);

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
            const userId = req.user?.id!;

            await postService.delete(id, userId);

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

export default postController;

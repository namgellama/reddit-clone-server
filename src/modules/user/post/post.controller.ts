import { NextFunction, Request, Response } from 'express';
import userPostService from './post.service';
import { sendResponse } from '@/utils/response.utils';

const userPostController = {
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

import { NextFunction, Request, Response } from 'express';

import { sendResponse } from '@/shared/utils/response.utils';
import userService from './user.service';

const userController = {
    // Get me
    getMe: async (req: Request, res: Response, next: NextFunction) => {
        try {
            const user = await userService.getMe(req);

            sendResponse(res, 'Current user fetched successfully', user);
        } catch (error) {
            next(error);
        }
    },
};

export default userController;

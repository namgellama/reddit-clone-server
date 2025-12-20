import { NextFunction, Request, Response } from 'express';

import { sendResponse } from '@/shared/utils/response.utils';
import upvoteService from './upvote.service';
import { IToggleUpvoteInput } from './upvote.validation';

const upvoteController = {
    // Toggle upvote
    toggle: async (
        req: Request<{}, {}, IToggleUpvoteInput>,
        res: Response,
        next: NextFunction
    ) => {
        try {
            const body = req.body;
            const userId = req.user!.id;

            const result = await upvoteService.toggle(body, userId);

            sendResponse(res, 'Upvote toggled successfully', result);
        } catch (error) {
            next(error);
        }
    },
};

export default upvoteController;

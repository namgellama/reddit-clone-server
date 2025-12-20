import { NextFunction, Request, Response } from 'express';

import { sendResponse } from '@/shared/utils/response.utils';
import downvoteService from './downvote.service';
import { IToggleDownvoteInput } from './downvote.validation';

const downvoteController = {
    // Toggle downvote
    toggle: async (
        req: Request<{}, {}, IToggleDownvoteInput>,
        res: Response,
        next: NextFunction
    ) => {
        try {
            const body = req.body;
            const userId = req.user!.id;

            const result = await downvoteService.toggle(body, userId);

            sendResponse(res, 'Downvote toggled successfully', result);
        } catch (error) {
            next(error);
        }
    },
};

export default downvoteController;

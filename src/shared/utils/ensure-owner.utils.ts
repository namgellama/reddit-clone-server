import { StatusCodes } from 'http-status-codes';

import { ApiError } from './error.utils';

export const ensureOwner = (authorId: string, userId: string) => {
    if (authorId !== userId)
        throw new ApiError('Not allowed', StatusCodes.FORBIDDEN);
};

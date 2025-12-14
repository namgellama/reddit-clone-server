import { Response } from 'express';
import { StatusCodes } from 'http-status-codes';

export const sendResponse = <T>(
    res: Response,
    message: string,
    data?: T,
    statusCode: number = StatusCodes.OK
) => {
    const response: {
        success: true;
        message: string;
        data?: T;
    } = {
        success: true,
        message,
    };

    if (data !== undefined) {
        response.data = data;
    }

    return res.status(statusCode).json(response);
};

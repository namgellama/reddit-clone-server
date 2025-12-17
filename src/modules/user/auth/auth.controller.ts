import { NextFunction, Request, Response } from 'express';
import { StatusCodes } from 'http-status-codes';

import { sendResponse } from '@/shared/utils/response.utils';
import { ICreateUserInput } from '../user/user.validation';
import authService from './auth.service';
import { ILoginUserInput } from './auth.validation';

const authController = {
    // Register
    register: async (
        req: Request<{}, {}, ICreateUserInput>,
        res: Response,
        next: NextFunction
    ) => {
        try {
            const newUser = await authService.register(req.body);

            sendResponse(
                res,
                'User registered successfully',
                newUser,
                StatusCodes.CREATED
            );
        } catch (error) {
            next(error);
        }
    },

    // Login
    login: async (
        req: Request<{}, {}, ILoginUserInput>,
        res: Response,
        next: NextFunction
    ) => {
        try {
            const { accessToken } = await authService.login(res, req.body);

            sendResponse(res, 'User logged in successfully', { accessToken });
        } catch (error) {
            next(error);
        }
    },
};

export default authController;

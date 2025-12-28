import { NextFunction, Request, Response } from 'express';
import { StatusCodes } from 'http-status-codes';

import { User } from '@/generated/prisma';
import { sendResponse } from '@/shared/utils/response.utils';
import { ICreateUserInput } from '../user/user.validation';
import authService from './auth.service';
import { ILoginUserInput, IRegisterEmailInput } from './auth.validation';

const authController = {
    // Sign up - Register email
    registerEmail: async (
        req: Request<{}, {}, IRegisterEmailInput>,
        res: Response,
        next: NextFunction
    ) => {
        try {
            const body = req.body;

            await authService.registerEmail(body);

            sendResponse(res, 'OTP sent to email');
        } catch (error) {
            next(error);
        }
    },

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

    // Logout
    logout: (req: Request, res: Response, next: NextFunction) => {
        try {
            authService.logout(res);

            sendResponse(res, 'User logged out successfully', {});
        } catch (error) {
            next(error);
        }
    },

    // Refresh token
    refreshToken: (req: Request, res: Response, next: NextFunction) => {
        try {
            const user = req.user as User;

            const { accessToken } = authService.refreshToken(res, user.id);

            sendResponse(res, 'Token refreshed successfully', { accessToken });
        } catch (error) {
            next(error);
        }
    },
};

export default authController;

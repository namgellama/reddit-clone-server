import { Response } from 'express';
import { StatusCodes } from 'http-status-codes';

import { signJwt } from '@/shared/lib/jwt';
import {
    comparePassword,
    hashPassword,
    setRefreshToken,
} from '@/shared/utils/auth.utils';
import { ApiError } from '@/shared/utils/error.utils';
import userService from '../user/user.service';
import { ICreateUserInput } from '../user/user.validation';
import { ILoginUserInput } from './auth.validation';

const authService = {
    // Register
    register: async (body: ICreateUserInput) => {
        const { email, username, firstName, lastName, password } = body;

        const existingEmail = await userService.getByEmail(email);
        const existingUsername = await userService.getByUsername(username);

        if (existingEmail)
            throw new ApiError('Email already exists', StatusCodes.CONFLICT);

        if (existingUsername)
            throw new ApiError('Username already exists', StatusCodes.CONFLICT);

        const hashedPassword = await hashPassword(body.password);

        return await userService.create({
            email,
            username,
            firstName,
            lastName,
            password: hashedPassword,
        });
    },

    // Login
    login: async (res: Response, body: ILoginUserInput) => {
        const { email, password } = body;

        const existingUser = await userService.getByEmail(email);

        if (!existingUser)
            throw new ApiError('Invalid credentials', StatusCodes.UNAUTHORIZED);

        const isMatch = await comparePassword(password, existingUser.password!);

        if (!isMatch)
            throw new ApiError('Invalid credentials', StatusCodes.UNAUTHORIZED);

        const accessToken = signJwt(
            { sub: existingUser.id, type: 'access' },
            'access'
        );
        const refreshToken = signJwt(
            { sub: existingUser.id, type: 'refresh' },
            'refresh'
        );

        setRefreshToken(res, refreshToken);

        return { accessToken };
    },

    // Refresh token
    refreshToken: async (res: Response, userId: string) => {
        const accessToken = signJwt({ sub: userId, type: 'access' }, 'access');

        return { accessToken };
    },
};

export default authService;

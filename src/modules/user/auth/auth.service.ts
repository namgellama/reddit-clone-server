import { Response } from 'express';
import { StatusCodes } from 'http-status-codes';

import { config } from '@/shared/config';
import { transporter } from '@/shared/config/nodemailer';
import { redis } from '@/shared/config/redis';
import { signJwt } from '@/shared/lib/jwt';
import {
    clearRefreshToken,
    comparePassword,
    hashPassword,
    setRefreshToken,
} from '@/shared/utils/auth.utils';
import { ApiError } from '@/shared/utils/error.utils';
import { generateOtp } from '@/shared/utils/otp.utils';
import userService from '../user/user.service';
import { ICreateUserInput } from '../user/user.validation';
import {
    ILoginUserInput,
    IRegisterEmailInput,
    IVerifyEmailInput,
} from './auth.validation';

const authService = {
    // Sign up - Register email
    registerEmail: async (body: IRegisterEmailInput) => {
        const { email } = body;

        const existingEmail = await userService.getByEmail(email);

        if (existingEmail)
            throw new ApiError('Email already exists', StatusCodes.CONFLICT);

        const otp = generateOtp();

        await redis.set(
            `signup:${email}`,
            JSON.stringify({
                otp,
            }),

            { expiration: { type: 'EX', value: 600 } }
        );

        await transporter.sendMail({
            from: `"REDDIT CLONE" <${config.nodemailer.email}>`,
            to: email,
            subject: 'Verify your email',
            html: `
                <h2>Email Verification</h2>
                <p>Your OTP:</p>
                <h1>${otp}</h1>
                <p>Expires in 10 minutes.</p>
            `,
        });
    },

    // Sign up - Verify email
    verifyEmail: async (body: IVerifyEmailInput) => {
        const { email, otp } = body;

        const key = `signup:${email}`;
        const data = await redis.get(key);

        if (!data)
            throw new ApiError(
                'OTP expired or not found',
                StatusCodes.BAD_REQUEST
            );

        const parsed = JSON.parse(data);

        if (Number(parsed.otp) !== otp)
            throw new ApiError('Invalid OTP', StatusCodes.BAD_REQUEST);
    },

    // Register
    register: async (body: ICreateUserInput) => {
        const { email, username, password } = body;

        const existingEmail = await userService.getByEmail(email);
        const existingUsername = await userService.getByUsername(username);

        if (existingEmail)
            throw new ApiError('Email already exists', StatusCodes.CONFLICT);

        if (existingUsername)
            throw new ApiError('Username already exists', StatusCodes.CONFLICT);

        const hashedPassword = await hashPassword(password);

        return await userService.create({
            email,
            username,
            password: hashedPassword,
            provider: 'LOCAL',
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

    // Logout
    logout: (res: Response) => {
        clearRefreshToken(res);
    },

    // Refresh token
    refreshToken: (res: Response, userId: string) => {
        const accessToken = signJwt({ sub: userId, type: 'access' }, 'access');

        return { accessToken };
    },

    // Google login
    googleLogin: async (res: Response, userId: string) => {
        const accessToken = signJwt({ sub: userId, type: 'access' }, 'access');
        const refreshToken = signJwt(
            { sub: userId, type: 'refresh' },
            'refresh'
        );

        setRefreshToken(res, refreshToken);

        return { accessToken };
    },
};

export default authService;

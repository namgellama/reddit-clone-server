import bcrypt from 'bcryptjs';
import { Response } from 'express';
import ms, { StringValue } from 'ms';

import { config } from '@/shared/config';

export const hashPassword = async (password: string) => {
    return await bcrypt.hash(password, 10);
};

export const comparePassword = async (
    password: string,
    hashedPassword: string
) => {
    return await bcrypt.compare(password, hashedPassword);
};

export const setRefreshToken = (res: Response, token: string) => {
    res.cookie('refreshToken', token, {
        httpOnly: true,
        secure: config.server.nodeEnv === 'production',
        sameSite: config.server.nodeEnv === 'production' ? 'none' : 'lax',
        maxAge: ms(config.jwt.refreshExpiry as StringValue),
    });
};

export const clearRefreshToken = (res: Response) => {
    res.clearCookie('refreshToken', {
        httpOnly: true,
        secure: config.server.nodeEnv === 'production',
        sameSite: config.server.nodeEnv === 'production' ? 'none' : 'lax',
    });
};

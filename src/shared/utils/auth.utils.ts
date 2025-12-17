import bcrypt from 'bcryptjs';
import { Response } from 'express';
import ms, { StringValue } from 'ms';

import { config } from '@/shared/config';
import { TokenType } from '@/shared/lib/jwt';

export const hashPassword = async (password: string) => {
    return await bcrypt.hash(password, 10);
};

export const comparePassword = async (
    password: string,
    hashedPassword: string
) => {
    return await bcrypt.compare(password, hashedPassword);
};

export const setToken = (
    res: Response,
    token: string,
    tokenType: TokenType
) => {
    res.cookie(tokenType === 'access' ? 'accessToken' : 'refreshToken', token, {
        httpOnly: true,
        secure: config.server.nodeEnv === 'production',
        sameSite: config.server.nodeEnv === 'production' ? 'none' : 'lax',
        maxAge:
            tokenType === 'access'
                ? ms(config.jwt.accessExpiry as StringValue)
                : ms(config.jwt.refreshExpiry as StringValue),
    });
};

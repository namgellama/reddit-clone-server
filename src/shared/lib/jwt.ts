import jwt from 'jsonwebtoken';
import ms, { StringValue } from 'ms';

import { config } from '@/shared/config';

export type TokenType = 'access' | 'refresh';

interface JwtPayload {
    sub: string;
    type: 'access' | 'refresh';
}

const getSecret = (tokenType: TokenType) => {
    if (tokenType === 'access') return config.jwt.accessSecret;

    return config.jwt.refreshSecret;
};

const getExpiry = (tokenType: TokenType) => {
    if (tokenType === 'access') return config.jwt.accessExpiry;

    return config.jwt.refreshExpiry;
};

export const signJwt = (payload: JwtPayload, tokenType: TokenType) => {
    return jwt.sign(payload, getSecret(tokenType), {
        expiresIn: getExpiry(tokenType),
    });
};

export const verifyJwt = (
    token: string,
    tokenType: TokenType
): JwtPayload | null => {
    try {
        return jwt.verify(token, getSecret(tokenType)) as JwtPayload;
    } catch (error) {
        return null;
    }
};

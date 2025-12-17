import dotenv from 'dotenv';
import { StringValue } from 'ms';

import { validateEnv } from './env-validator';

dotenv.config();

const env = validateEnv();

export const config = {
    server: {
        port: parseInt(env.PORT, 10),
        nodeEnv: env.NODE_ENV,
    },
    database: { url: env.DATABASE_URL },
    google: {
        clientId: env.GOOGLE_CLIENT_ID,
        clientSecret: env.GOOGLE_CLIENT_SECRET,
        callbackUrl: env.GOOGLE_CALLBACK_URL,
        clientRedirectUrl: env.GOOGLE_CLIENT_REDIRECT_URL,
    },
    jwt: {
        accessSecret: env.JWT_ACCESS_SECRET,
        accessExpiry: env.JWT_ACCESS_EXPIRY as StringValue,
        refreshSecret: env.JWT_REFRESH_SECRET,
        refreshExpiry: env.JWT_REFRESH_EXPIRY as StringValue,
    },
};

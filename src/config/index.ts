import dotenv from 'dotenv';
import { validateEnv } from './env-validator';

dotenv.config();

const env = validateEnv();

export const config = {
    server: {
        port: parseInt(env.PORT, 10),
        nodeEnv: env.NODE_ENV,
    },
};

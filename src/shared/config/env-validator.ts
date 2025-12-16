import z from 'zod';

const envSchema = z.object({
    NODE_ENV: z
        .enum(['development', 'production', 'test'])
        .default('development'),
    PORT: z.string().default('8000'),
    DATABASE_URL: z.url(),
    GOOGLE_CLIENT_ID: z.string().nonempty('Google Client ID is required'),
    GOOGLE_CLIENT_SECRET: z.string().nonempty('Google Client ID is required'),
    GOOGLE_CALLBACK_URL: z.url(),
    GOOGLE_CLIENT_REDIRECT_URL: z.url(),
    JWT_ACCESS_SECRET: z
        .string()
        .min(32, 'JWT ACCESS SECRET must be at least 32 characters'),
    JWT_ACCESS_EXPIRY: z.string(),
    JWT_REFRESH_SECRET: z
        .string()
        .min(32, 'JWT REFRESH SECRET must be at least 32 characters'),
    JWT_REFRESH_EXPIRY: z.string(),
});

export const validateEnv = () => {
    const result = envSchema.safeParse(process.env);

    if (!result.success) {
        console.error('Invalid environment variables: ', result.error.format());
        process.exit(1);
    }

    return result.data;
};

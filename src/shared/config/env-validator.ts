import z from 'zod';

const envSchema = z.object({
    NODE_ENV: z
        .enum(['development', 'production', 'test'])
        .default('development'),
    PORT: z.string().default('8000'),
    DATABASE_URL: z.url(),
});

export const validateEnv = () => {
    const result = envSchema.safeParse(process.env);

    if (!result.success) {
        console.error(
            'Invalid environment variables: ',
            z.treeifyError(result.error)
        );
        process.exit(1);
    }

    return result.data;
};

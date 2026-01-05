import { z } from 'zod';

const createSchema = z
    .object({
        email: z.email().trim().nonempty('Email is required'),
        username: z.string().trim().nonempty('Username is required'),
        password: z.string().optional(),
    })
    .superRefine((data, ctx) => {
        const { password } = data;
        if (password !== undefined) {
            if (password.length < 5) {
                ctx.addIssue({
                    code: 'custom',
                    path: ['password'],
                    message: 'Password must be at least 5 characters long',
                });
            }
            if (!/[A-Z]/.test(password)) {
                ctx.addIssue({
                    code: 'custom',
                    path: ['password'],
                    message:
                        'Password must contain at least one uppercase letter',
                });
            }
            if (!/[0-9]/.test(password)) {
                ctx.addIssue({
                    code: 'custom',
                    path: ['password'],
                    message: 'Password must contain at least one number',
                });
            }
            if (!/[^A-Za-z0-9]/.test(password)) {
                ctx.addIssue({
                    code: 'custom',
                    path: ['password'],
                    message: 'Password must contain at least one symbol',
                });
            }
        }
    });

const userValidation = {
    createSchema,
};

export default userValidation;

export type ICreateUserInput = z.infer<typeof userValidation.createSchema>;

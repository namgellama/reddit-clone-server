import { z } from 'zod';

const createSchema = z.object({
    email: z.email().trim().nonempty('Email is required'),
    username: z.string().trim().nonempty('Username is required'),
    firstName: z
        .string()
        .trim()
        .min(3, 'First name must be at least 3 characters'),
    lastName: z
        .string()
        .trim()
        .min(3, 'Last name must be at least 3 characters'),
    password: z
        .string()
        .min(5, 'Password must be at least 5 characters long')
        .regex(/[A-Z]/, 'Password must contain at least one uppercase letter')
        .regex(/[0-9]/, 'Password must contain at least one number')
        .regex(/[^A-Za-z0-9]/, 'Password must contain at least one symbol'),
});

const userValidation = {
    createSchema,
};

export default userValidation;

export type ICreateUserInput = z.infer<typeof userValidation.createSchema>;

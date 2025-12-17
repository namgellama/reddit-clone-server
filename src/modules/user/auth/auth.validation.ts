import z from 'zod';

const loginSchema = z.object({
    email: z.email().nonempty('Email is required'),
    password: z.string().nonempty('Password is required'),
});

const authValidation = {
    loginSchema,
};

export default authValidation;

export type ILoginUserInput = z.infer<typeof authValidation.loginSchema>;

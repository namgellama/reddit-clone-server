import z from 'zod';

const loginSchema = z.object({
    email: z.email().trim().nonempty('Email is required'),
    password: z.string().nonempty('Password is required'),
});

const registerEmail = z.object({
    email: z.email().trim().nonempty('Email is required'),
});

const authValidation = {
    loginSchema,
    registerEmail,
};

export default authValidation;

export type IRegisterEmailInput = z.infer<typeof authValidation.registerEmail>;
export type ILoginUserInput = z.infer<typeof authValidation.loginSchema>;

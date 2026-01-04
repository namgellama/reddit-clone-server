import z from 'zod';

// Sign up - register email
const registerEmail = z.object({
    email: z.email().trim().nonempty('Email is required'),
});

// Sign up - verify email
const verifyEmail = z.object({
    email: z.email().trim().nonempty('Email is required'),
    otp: z.coerce
        .number()
        .int('OTP must be an integer')
        .min(100000, 'OTP must be 6 digits')
        .max(999999, 'OTP must be 6 digits'),
});

// Login
const loginSchema = z.object({
    email: z.email().trim().nonempty('Email is required'),
    password: z.string().nonempty('Password is required'),
});

const authValidation = {
    registerEmail,
    verifyEmail,
    loginSchema,
};

export default authValidation;

export type IRegisterEmailInput = z.infer<typeof authValidation.registerEmail>;
export type IVerifyEmailInput = z.infer<typeof authValidation.verifyEmail>;
export type ILoginUserInput = z.infer<typeof authValidation.loginSchema>;

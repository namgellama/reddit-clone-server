import { Router } from 'express';

import { refreshProtect } from '@/shared/middlewares/auth.middleware';
import { validate } from '@/shared/middlewares/validate.middleware';
import passport from 'passport';
import userValidation from '../user/user.validation';
import authController from './auth.controller';
import authValidation from './auth.validation';

const router = Router();

router.post(
    '/register',
    validate(userValidation.createSchema),
    authController.register
);

router.post(
    '/signup/register-email',
    validate(authValidation.registerEmail),
    authController.registerEmail
);

router.post(
    '/signup/verify-email',
    validate(authValidation.verifyEmail),
    authController.verifyEmail
);

router.post(
    '/login',
    validate(authValidation.loginSchema),
    authController.login
);

router.post('/logout', authController.logout);

router.post('/refresh-token', refreshProtect, authController.refreshToken);

router.get(
    '/google',
    passport.authenticate('google', { scope: ['profile', 'email'] })
);

router.get(
    '/google/callback',
    passport.authenticate('google', {
        session: false,
    }),
    authController.googleLogin
);

export { router as authRoutes };

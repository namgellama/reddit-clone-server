import { Router } from 'express';

import { refreshProtect } from '@/shared/middlewares/auth.middleware';
import { validate } from '@/shared/middlewares/validate.middleware';
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
    '/login',
    validate(authValidation.loginSchema),
    authController.login
);

router.post('/refresh-token', refreshProtect, authController.refreshToken);

export { router as authRoutes };

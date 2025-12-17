import { Router } from 'express';

import { validate } from '@/shared/middlewares/validate.middleware';
import userValidation from '../user/user.validation';
import authController from './auth.controller';

const router = Router();

router.post(
    '/register',
    validate(userValidation.createSchema),
    authController.register
);

export { router as authRoutes };

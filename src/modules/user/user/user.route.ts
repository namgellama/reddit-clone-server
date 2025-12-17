import { Router } from 'express';

import { protect } from '@/shared/middlewares/auth.middleware';
import userController from './user.controller';

const router = Router();

router.get('/get-me', protect, userController.getMe);

export { router as userRoutes };

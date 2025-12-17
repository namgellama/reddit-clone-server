import { Router } from 'express';

import userController from './user.controller';

const router = Router();

router.get('/get-me', userController.getMe);

export { router as userRoutes };

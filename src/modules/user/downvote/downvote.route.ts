import { Router } from 'express';

import { protect } from '@/shared/middlewares/auth.middleware';
import downvoteController from './downvote.controller';

const router = Router();

router.post('/', protect, downvoteController.toggle);

export { router as downvoteRoutes };

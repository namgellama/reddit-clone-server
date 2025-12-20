import { Router } from 'express';
import upvoteController from './upvote.controller';
import { protect } from '@/shared/middlewares/auth.middleware';

const router = Router();

router.post('/', protect, upvoteController.toggle);

export { router as upvoteRoutes };

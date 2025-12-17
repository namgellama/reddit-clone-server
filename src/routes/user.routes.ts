import { Router } from 'express';

import { authRoutes } from '@/modules/user/auth/auth.route';
import { postRoutes } from '@/modules/user/post/post.route';
import { userRoutes } from '@/modules/user/user/user.route';
import { protect } from '@/shared/middlewares/auth.middleware';

const router = Router();

router.use('/auth', authRoutes);
router.use('/posts', postRoutes);
router.use('/users', protect, userRoutes);

export { router as userRoutes };

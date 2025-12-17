import { Router } from 'express';

import { authRoutes } from '@/modules/user/auth/auth.route';
import { postRoutes } from '@/modules/user/post/post.route';
import { userRoutes } from '@/modules/user/user/user.route';

const router = Router();

router.use('/auth', authRoutes);
router.use('/posts', postRoutes);
router.use('/users', userRoutes);

export { router as userRoutes };

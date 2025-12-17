import { Router } from 'express';

import { authRoutes } from '@/modules/user/auth/auth.route';
import { postRoutes } from '@/modules/user/post/post.route';

const router = Router();

router.use('/auth', authRoutes);
router.use('/posts', postRoutes);

export { router as userRoutes };

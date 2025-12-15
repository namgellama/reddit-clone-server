import { Router } from 'express';

import { postRoutes } from '@/modules/user/post/post.route';

const router = Router();

router.use('/posts', postRoutes);

export { router as userRoutes };

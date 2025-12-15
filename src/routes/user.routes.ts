import { Router } from 'express';

import { userPostRoutes } from '@/modules/user/post/post.route';

const router = Router();

router.use('/posts', userPostRoutes);

export { router as userRoutes };

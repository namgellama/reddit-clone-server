import { Router } from 'express';

import { authRoutes } from '@/modules/user/auth/auth.route';
import { commentRoutes } from '@/modules/user/comment/comment.route';
import { downvoteRoutes } from '@/modules/user/downvote/downvote.route';
import { postRoutes } from '@/modules/user/post/post.route';
import { upvoteRoutes } from '@/modules/user/upvote/upvote.route';
import { userRoutes } from '@/modules/user/user/user.route';
import { protect } from '@/shared/middlewares/auth.middleware';

const router = Router();

router.use('/auth', authRoutes);
router.use('/users', protect, userRoutes);
router.use('/posts', postRoutes);
router.use('/posts/:postId/comments', commentRoutes);
router.use('/upvotes', upvoteRoutes);
router.use('/downvotes', downvoteRoutes);

export { router as userRoutes };

import { Router } from 'express';

import { protect } from '@/shared/middlewares/auth.middleware';
import { validate } from '@/shared/middlewares/validate.middleware';
import commentController from './comment.controller';
import commentValidation from './comment.validation';

const router = Router({ mergeParams: true });

router.post(
    '/',
    protect,
    validate(commentValidation.createSchema),
    commentController.create
);

router.post(
    '/:commentId/replies',
    protect,
    validate(commentValidation.createSchema),
    commentController.reply
);

router.get('/', protect, commentController.getAll);

router.get('/:commentId/replies', protect, commentController.getAllReplies);

router.get('/:commentId', protect, commentController.getById);

router.get('/:commentId', protect, commentController.getById);

router.put('/:commentId', protect, commentController.update);

export { router as commentRoutes };

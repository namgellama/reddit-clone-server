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

export { router as commentRoutes };

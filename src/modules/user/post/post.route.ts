import { Router } from 'express';

import { protect } from '@/shared/middlewares/auth.middleware';
import { validate } from '@/shared/middlewares/validate.middleware';
import commonValidation from '@/shared/validations/common.validation';
import postController from './post.controller';
import postValidation from './post.validations';

const router = Router();

router.post(
    '/',
    protect,
    validate(postValidation.createSchema),
    postController.create
);

router.get('/', postController.getAll);

router.get(
    '/:id',
    validate(commonValidation.idParamsSchema, 'params'),
    postController.getById
);

router.put(
    '/:id',
    protect,
    validate(commonValidation.idParamsSchema, 'params'),
    validate(postValidation.createSchema),
    postController.update
);

router.delete(
    '/:id',
    protect,
    validate(commonValidation.idParamsSchema, 'params'),
    postController.delete
);

export { router as postRoutes };

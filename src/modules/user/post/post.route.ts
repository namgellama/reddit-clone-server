import { Router } from 'express';

import { protect } from '@/shared/middlewares/auth.middleware';
import { validate } from '@/shared/middlewares/validate.middleware';
import commonValidation from '@/shared/validations/common.validation';
import userPostController from './post.controller';
import userPostValidation from './post.validations';

const router = Router();

router.post(
    '/',
    protect,
    validate(userPostValidation.createSchema),
    userPostController.create
);

router.get('/', userPostController.getAll);

router.get(
    '/:id',
    validate(commonValidation.idParamsSchema, 'params'),
    userPostController.getById
);

router.put(
    '/:id',
    protect,
    validate(commonValidation.idParamsSchema, 'params'),
    validate(userPostValidation.createSchema),
    userPostController.update
);

router.delete(
    '/:id',
    protect,
    validate(commonValidation.idParamsSchema, 'params'),
    userPostController.delete
);

export { router as postRoutes };

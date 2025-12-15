import { Router } from 'express';

import { validate } from '@/shared/middlewares/validate.middleware';
import userPostController from './post.controller';
import postValidation from './post.validations';
import commonValidation from '@/shared/validations/common.validation';

const router = Router();

router.post(
    '/',
    validate(postValidation.createSchema),
    userPostController.create
);

router.get('/', userPostController.getAll);

router.get(
    '/:id',
    validate(commonValidation.idParamsSchema, 'params'),
    userPostController.getById
);

export { router as userPostRoutes };

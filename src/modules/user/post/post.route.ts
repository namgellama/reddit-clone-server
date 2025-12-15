import { Router } from 'express';

import { validate } from '@/middlewares/validate.middleware';
import userPostController from './post.controller';
import postValidation from './post.validations';

const router = Router();

router.get('/', userPostController.getAll);

router.post(
    '/',
    validate(postValidation.createSchema),
    userPostController.create
);

export { router as userPostRoutes };

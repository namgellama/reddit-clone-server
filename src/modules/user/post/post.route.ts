import { Router } from 'express';

import userPostController from './post.controller';

const router = Router();

router.get('/', userPostController.getAll);

export { router as userPostRoutes };

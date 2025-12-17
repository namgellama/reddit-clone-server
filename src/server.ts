import cookieParser from 'cookie-parser';
import cors from 'cors';
import dotenv from 'dotenv';
import express, { Request, Response } from 'express';
import { createServer } from 'http';
import { StatusCodes } from 'http-status-codes';

import { indexRoutes } from '@/routes';
import { config } from '@/shared/config';
import passport from '@/shared/config/passport-access';
import { logger } from '@/shared/lib/logger';
import {
    errorHandler,
    notFoundHandler,
} from '@/shared/middlewares/error.middleware';

dotenv.config();

const app = express();
const server = createServer(app);

app.use(cors({ origin: 'http://localhost:5173', credentials: true }));
app.use(express.json());
app.use(cookieParser());
app.use(passport.initialize());

// Routes
app.use('/api/ping', (req: Request, res: Response) => {
    res.status(StatusCodes.OK).json({ message: 'Pong!' });
});

app.use('/api/v1', indexRoutes);

// 404 Handler
app.use(notFoundHandler);

// General Error Handler
app.use(errorHandler);

const startServer = async () => {
    try {
        server.listen(config.server.port, () => {
            logger.info(
                `Server running on ${config.server.nodeEnv} mode on port ${config.server.port}`
            );
        });
    } catch (error) {
        console.error('Failed to start server: ', error);
        process.exit(1);
    }
};

startServer();

import express, { Request, Response } from 'express';
import dotenv from 'dotenv';
import { createServer } from 'http';
import { config } from './config';
import { StatusCodes } from 'http-status-codes';
import { errorHandler, notFoundHandler } from './middlewares/error.middleware';
import { logger } from './utils/logger.utils';

dotenv.config();

const app = express();
const server = createServer(app);

// Routes
app.use('/api/ping', (req: Request, res: Response) => {
    res.status(StatusCodes.OK).json({ message: 'Pong!' });
});

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

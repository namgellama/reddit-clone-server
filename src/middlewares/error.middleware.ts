import { config } from '@/config';
import { NextFunction, Request, Response } from 'express';
import { StatusCodes } from 'http-status-codes';

export interface AppError extends Error {
    statusCode?: number;
    errors?: { path: string; message: string }[];
    req?: { url?: string; method?: string };
    status?: number;
    statusText?: string;
    err?: string;
}

/**
 * 404 Not Found Handler
 */
export const notFoundHandler = (req: Request, res: Response) => {
    res.status(StatusCodes.NOT_FOUND).json({
        success: false,
        message: `Route not found: ${req.originalUrl}`,
    });
};

/**
 * Global Error Handler
 */
export const errorHandler = (
    err: AppError,
    _req: Request,
    res: Response,
    next: NextFunction
) => {
    const statusCode = err.statusCode || 500;
    const message = err.message || 'Internal server error';

    res.status(statusCode).json({
        success: false,
        message,
        ...(err.errors && { errors: err.errors }),
        ...(config.server.nodeEnv === 'development' && { stack: err.stack }),
    });
};

import { Request, Response, NextFunction } from 'express';
import { AppError } from './error.middleware';
import { ZodType } from 'zod';

interface ValidationErrorItem {
    path: string;
    message: string;
}

export class ValidationError extends Error implements AppError {
    statusCode = 400;
    errors: ValidationErrorItem[];

    constructor(errors: ValidationErrorItem[]) {
        super('Validation error');
        this.name = 'ValidationError';
        this.errors = errors;
    }
}

export const validate =
    (schema: ZodType<any>, property: 'body' | 'query' | 'params' = 'body') =>
    (req: Request, _res: Response, next: NextFunction) => {
        const result = schema.safeParse(req[property]);
        if (!result.success) {
            const formattedErrors: ValidationErrorItem[] =
                result.error.issues.map((e) => ({
                    path: e.path.join('.'),
                    message: e.message,
                }));

            return next(new ValidationError(formattedErrors));
        }

        Object.assign(req[property], result.data);
        next();
    };

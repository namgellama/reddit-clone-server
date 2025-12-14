export interface FieldError {
    path: string;
    message: string;
}

export class ApiError extends Error {
    public statusCode: number;
    public errors?: FieldError[];

    constructor(message: string, statusCode = 500, errors?: FieldError[]) {
        super(message);
        this.name = 'ApiError';
        this.statusCode = statusCode;
        this.errors = errors;

        // Maintains proper stack trace in V8
        if (Error.captureStackTrace) {
            Error.captureStackTrace(this, ApiError);
        }
    }
}

// Reusable helper
export const apiError = (
    statusCode: number,
    message: string,
    errors?: FieldError[]
): ApiError => {
    return new ApiError(message, statusCode, errors);
};

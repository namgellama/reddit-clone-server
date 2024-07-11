import { NextFunction, Request, Response } from "express";

const notFound = (request: Request, response: Response, next: NextFunction) => {
	const error = new Error(`Not Found - ${request.originalUrl}`);
	response.status(404);
	next(error);
};

const errorHandler = (
	error: Error,
	request: Request,
	response: Response,
	next: NextFunction
) => {
	let statusCode = response.statusCode === 200 ? 500 : response.statusCode;
	let message = error.message;

	response.status(statusCode).json({
		message,
		stack: process.env.NODE_ENV === "production" ? "" : error.stack,
	});
};

export { errorHandler, notFound };

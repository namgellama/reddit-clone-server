import { NextFunction, Request, Response } from "express";

const asyncHandler =
	(fn: Function) =>
	(request: Request, response: Response, next: NextFunction) => {
		Promise.resolve(fn(request, response, next)).catch(next);
	};

export default asyncHandler;

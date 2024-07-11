import prisma from "@prismaClient";
import { Request, Response } from "express";
import asyncHandler from "@middlewares/asyncHandler";

const getPosts = asyncHandler(async (request: Request, response: Response) => {
	const posts = await prisma.post.findMany();
	response.status(200).json(posts);
});

export { getPosts };

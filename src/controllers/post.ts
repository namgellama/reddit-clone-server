import asyncHandler from "@/middlewares/asyncHandler";
import { Request, Response } from "express";
import prisma from "@prismaClient";

const getPosts = asyncHandler(async (request: Request, response: Response) => {
	const posts = await prisma.post.findMany();
	response.status(200).json(posts);
});

export { getPosts };

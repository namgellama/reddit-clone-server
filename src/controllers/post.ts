import prisma from "@prismaClient";
import { Request, Response } from "express";
import asyncHandler from "@middlewares/asyncHandler";
import { PostRequestDTO } from "@/dtos/post";

const getPosts = asyncHandler(async (request: Request, response: Response) => {
	const posts = await prisma.post.findMany();
	response.status(200).json(posts);
});

const createPost = asyncHandler(
	async (request: Request<{}, {}, PostRequestDTO>, response: Response) => {
		const { title, body } = request.body;

		const newPost = await prisma.post.create({
			data: { title, body },
		});

		response.status(201).json(newPost);
	}
);

export { getPosts, createPost };

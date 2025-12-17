import { StatusCodes } from 'http-status-codes';

import { prisma } from '@/shared/lib/prisma';
import { ensureOwner } from '@/shared/utils/ensure-owner.utils';
import { apiError } from '@/shared/utils/error.utils';
import { ICreatePostInput } from './post.validations';

const postService = {
    // Create
    create: async (body: ICreatePostInput, userId: string) => {
        return await prisma.post.create({
            data: {
                ...body,
                userId,
            },
        });
    },

    // Get all
    getAll: async () => {
        return await prisma.post.findMany();
    },

    // Get by id
    getById: async (id: string) => {
        const existingPost = await prisma.post.findUnique({ where: { id } });

        if (!existingPost)
            throw apiError(StatusCodes.NOT_FOUND, 'Post not found');

        return existingPost;
    },

    // Update
    update: async (id: string, body: ICreatePostInput, userId: string) => {
        const existingPost = await postService.getById(id);
        ensureOwner(existingPost.userId, userId);

        return await prisma.post.update({ where: { id, userId }, data: body });
    },

    // Delete
    delete: async (id: string, userId: string) => {
        const existingPost = await postService.getById(id);
        ensureOwner(existingPost.id, userId);

        await prisma.post.delete({ where: { id } });
    },
};

export default postService;

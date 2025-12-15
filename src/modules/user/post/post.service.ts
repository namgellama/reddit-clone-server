import { StatusCodes } from 'http-status-codes';

import { prisma } from '@/shared/lib/prisma';
import { ICreatePostInput } from './post.validations';
import { apiError } from '@/shared/utils/error.utils';

const userPostService = {
    // Create
    create: async (body: ICreatePostInput) => {
        return await prisma.post.create({
            data: body,
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
    update: async (id: string, body: ICreatePostInput) => {
        await userPostService.getById(id);

        return await prisma.post.update({ where: { id }, data: body });
    },

    // Delete
    delete: async (id: string) => {
        await userPostService.getById(id);

        await prisma.post.delete({ where: { id } });
    },
};

export default userPostService;

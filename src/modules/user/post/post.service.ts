import { prisma } from '@/shared/lib/prisma';
import { ICreatePostInput } from './post.validations';
import { apiError } from '@/shared/utils/error.utils';
import { StatusCodes } from 'http-status-codes';

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
};

export default userPostService;

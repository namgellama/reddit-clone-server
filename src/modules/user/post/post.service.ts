import { prisma } from '@/lib/prisma';
import { ICreatePostInput } from './post.validations';

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
};

export default userPostService;

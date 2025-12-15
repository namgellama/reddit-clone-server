import { prisma } from '@/lib/prisma';

const userPostService = {
    getAll: async () => {
        return await prisma.post.findMany();
    },
};

export default userPostService;

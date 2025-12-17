import { Request } from 'express';

import { prisma } from '@/shared/lib/prisma';
import { ICreateUserInput } from './user.validation';

const userService = {
    // Create
    create: async (body: ICreateUserInput) => {
        const { password, ...rest } = await prisma.user.create({ data: body });

        return rest;
    },

    // Get by id
    getById: async (id: string) => {
        return await prisma.user.findUnique({ where: { id } });
    },

    // Get by Email
    getByEmail: async (email: string) => {
        return await prisma.user.findUnique({ where: { email } });
    },

    // Get by username
    getByUsername: async (username: string) => {
        return await prisma.user.findUnique({ where: { username } });
    },

    // Get me
    getMe: async (req: Request) => {
        return req.user;
    },
};

export default userService;

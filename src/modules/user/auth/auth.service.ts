import { StatusCodes } from 'http-status-codes';

import { hashPassword } from '@/shared/utils/auth.utils';
import { ApiError } from '@/shared/utils/error.utils';
import userService from '../user/user.service';
import { ICreateUserInput } from '../user/user.validation';

const authService = {
    // Register
    register: async (body: ICreateUserInput) => {
        const { email, username, firstName, lastName, password } = body;

        const existingEmail = await userService.getByEmail(email);
        const existingUsername = await userService.getByUsername(username);

        if (existingEmail)
            throw new ApiError('Email already exists', StatusCodes.CONFLICT);

        if (existingUsername)
            throw new ApiError('Username already exists', StatusCodes.CONFLICT);

        const hashedPassword = await hashPassword(body.password);

        return await userService.create({
            email,
            username,
            firstName,
            lastName,
            password: hashedPassword,
        });
    },
};

export default authService;

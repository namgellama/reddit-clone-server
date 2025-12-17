import { z } from 'zod';

const createSchema = z.object({
    title: z.string().min(3, 'Title must be at least 3 characters'),
    description: z.string().min(5, 'Description must be at least 5 characters'),
});

const postValidation = {
    createSchema,
};

export default postValidation;

export type ICreatePostInput = z.infer<typeof postValidation.createSchema>;

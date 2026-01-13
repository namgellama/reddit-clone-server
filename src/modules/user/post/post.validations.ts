import { z } from 'zod';

const createSchema = z.object({
    title: z.string().trim().min(3, 'Title must be at least 3 characters'),
    content: z.string().trim().min(5, 'Content must be at least 5 characters'),
});

const postValidation = {
    createSchema,
};

export default postValidation;

export type ICreatePostInput = z.infer<typeof postValidation.createSchema>;

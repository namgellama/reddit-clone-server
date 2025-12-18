import z from 'zod';

const createSchema = z.object({
    message: z.string().trim().nonempty('Message is required'),
});

const commentValidation = {
    createSchema,
};

export default commentValidation;

export type ICreateCommentInput = z.infer<
    typeof commentValidation.createSchema
>;

import z from 'zod';

const toggleSchema = z.object({
    entityId: z.uuid(),
    entityType: z.enum(['post', 'comment']),
});

const downvoteValidation = {
    toggleSchema,
};

export default downvoteValidation;

export type IToggleDownvoteInput = z.infer<
    typeof downvoteValidation.toggleSchema
>;

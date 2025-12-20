import z from 'zod';

const toggleSchema = z.object({
    entityId: z.uuid(),
    entityType: z.enum(['post', 'comment']),
});

const upvoteValidation = {
    toggleSchema,
};

export default upvoteValidation;

export type IToggleUpvoteInput = z.infer<typeof upvoteValidation.toggleSchema>;

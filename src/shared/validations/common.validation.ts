import z from 'zod';

const commonValidation = {
    idParamsSchema: z.object({
        id: z.uuid(),
    }),
};

export default commonValidation;

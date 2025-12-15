import z from 'zod';

const commonRules = {
    // Id schema
    idSchema: z.uuid(),
};

export default commonRules;

import { prisma } from '@/shared/lib/prisma';
import postService from '../post/post.service';
import { ICreateCommentInput } from './comment.validation';

const commentService = {
    // Create
    create: async (
        body: ICreateCommentInput,
        postId: string,
        userId: string
    ) => {
        await postService.getById(postId);

        return await prisma.comment.create({
            data: {
                ...body,
                postId,
                userId,
            },
        });
    },
};

export default commentService;

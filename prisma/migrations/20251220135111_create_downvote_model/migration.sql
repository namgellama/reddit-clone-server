-- CreateTable
CREATE TABLE "Downvote" (
    "id" TEXT NOT NULL,
    "postId" TEXT,
    "commentId" TEXT,
    "userId" TEXT NOT NULL,

    CONSTRAINT "Downvote_pkey" PRIMARY KEY ("id")
);

-- CreateIndex
CREATE INDEX "Downvote_postId_idx" ON "Downvote"("postId");

-- CreateIndex
CREATE INDEX "Downvote_commentId_idx" ON "Downvote"("commentId");

-- CreateIndex
CREATE UNIQUE INDEX "Downvote_userId_postId_key" ON "Downvote"("userId", "postId");

-- CreateIndex
CREATE UNIQUE INDEX "Downvote_userId_commentId_key" ON "Downvote"("userId", "commentId");

-- AddForeignKey
ALTER TABLE "Downvote" ADD CONSTRAINT "Downvote_postId_fkey" FOREIGN KEY ("postId") REFERENCES "Post"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "Downvote" ADD CONSTRAINT "Downvote_commentId_fkey" FOREIGN KEY ("commentId") REFERENCES "Comment"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "Downvote" ADD CONSTRAINT "Downvote_userId_fkey" FOREIGN KEY ("userId") REFERENCES "User"("id") ON DELETE CASCADE ON UPDATE CASCADE;

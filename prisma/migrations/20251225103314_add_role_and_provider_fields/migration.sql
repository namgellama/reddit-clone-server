-- CreateEnum
CREATE TYPE "UserRole" AS ENUM ('BLOGGER', 'ADMIN');

-- CreateEnum
CREATE TYPE "Provider" AS ENUM ('LOCAL', 'GOOGLE');

-- AlterTable
ALTER TABLE "User" ADD COLUMN     "provider" "Provider" NOT NULL DEFAULT 'LOCAL',
ADD COLUMN     "role" "UserRole" NOT NULL DEFAULT 'BLOGGER';

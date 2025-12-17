import { PrismaClient } from '@/generated/prisma/client';
import { config } from '@/shared/config';
import { PrismaPg } from '@prisma/adapter-pg';
import 'dotenv/config';

const connectionString = config.database.url;

const adapter = new PrismaPg({ connectionString });
const prisma = new PrismaClient({ adapter });

export { prisma };

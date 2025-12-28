import { createClient } from 'redis';

import { config } from '.';
import { logger } from '../lib/logger';

export const redis = createClient({
    url: config.redisUrl,
});

redis.on('error', (err) => logger.error('Redis Error', err));

redis.connect();

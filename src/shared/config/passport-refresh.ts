import { Request } from 'express';
import { JwtPayload } from 'jsonwebtoken';
import passport from 'passport';
import { Strategy as JwtStrategy } from 'passport-jwt';

import { prisma } from '@/shared/lib/prisma';
import { config } from '.';

passport.use(
    'refreshToken',
    new JwtStrategy(
        {
            jwtFromRequest: (req: Request) => req.cookies?.refreshToken,
            secretOrKey: config.jwt.refreshSecret,
        },
        async (payload: JwtPayload, done) => {
            try {
                const user = await prisma.user.findUnique({
                    where: { id: payload.sub },
                });

                if (!user) {
                    return done(null, false);
                }

                return done(null, user);
            } catch (error) {
                return done(error, false);
            }
        }
    )
);

export default passport;

import { Request } from 'express';
import { JwtPayload } from 'jsonwebtoken';
import passport from 'passport';
import { Strategy as JwtStrategy } from 'passport-jwt';

import userService from '@/modules/user/user/user.service';
import { config } from '..';

passport.use(
    'refreshToken',
    new JwtStrategy(
        {
            jwtFromRequest: (req: Request) => req.cookies?.refreshToken,
            secretOrKey: config.jwt.refreshSecret,
        },
        async (payload: JwtPayload, done) => {
            try {
                const user = await userService.getById(payload.sub!);

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

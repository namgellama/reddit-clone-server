import { JwtPayload } from 'jsonwebtoken';
import passport from 'passport';
import { ExtractJwt, Strategy as JwtStrategy } from 'passport-jwt';

import userService from '@/modules/user/user/user.service';
import { AuthUser } from '@/types/express';
import { config } from '..';

passport.use(
    'accessToken',
    new JwtStrategy(
        {
            jwtFromRequest: ExtractJwt.fromAuthHeaderAsBearerToken(),
            secretOrKey: config.jwt.accessSecret,
        },
        async (payload: JwtPayload, done) => {
            try {
                if (!payload.sub) return done(null, false);

                const user = await userService.getById(payload.sub);

                if (!user) {
                    return done(null, false);
                }

                const authUser: AuthUser = {
                    id: user.id,
                    email: user.email,
                    username: user.username,
                    firstName: user.firstName,
                    lastName: user.lastName,
                    createdAt: user.createdAt,
                    updatedAt: user.updatedAt,
                };

                return done(null, authUser);
            } catch (error) {
                return done(error, false);
            }
        }
    )
);

export default passport;

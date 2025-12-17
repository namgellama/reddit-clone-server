import { JwtPayload } from 'jsonwebtoken';
import passport from 'passport';
import { ExtractJwt, Strategy as JwtStrategy } from 'passport-jwt';

import userService from '@/modules/user/user/user.service';
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

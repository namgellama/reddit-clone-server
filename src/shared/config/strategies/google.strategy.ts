import passport from 'passport';
import { Strategy as GoogleStrategy } from 'passport-google-oauth20';

import userService from '@/modules/user/user/user.service';
import { config } from '@/shared/config';

passport.use(
    new GoogleStrategy(
        {
            clientID: config.google.clientId,
            clientSecret: config.google.clientSecret,
            callbackURL: config.google.callbackUrl,
        },
        async (_, __, profile, done) => {
            try {
                let user;

                user = await userService.getByEmail(profile.emails?.[0].value!);

                if (!user)
                    user = await userService.create({
                        email: profile.emails?.[0].value!,
                        firstName: profile.name?.givenName || '',
                        lastName: profile.name?.familyName || '',
                        username:
                            profile.emails?.[0].value!.split('@')[0] || '',
                        provider: 'GOOGLE',
                    });

                return done(null, user);
            } catch (error) {
                done(error, false);
            }
        }
    )
);

export default passport;

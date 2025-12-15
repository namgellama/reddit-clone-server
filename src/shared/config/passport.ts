import { prisma } from '@/shared/lib/prisma';
import passport from 'passport';
import { Strategy as GoogleStrategy } from 'passport-google-oauth20';
import { config } from '.';

passport.use(
    new GoogleStrategy(
        {
            clientID: config.google.clientId,
            clientSecret: config.google.clientSecret,
            callbackURL: config.google.callbackUrl,
        },
        async (accessToken, refreshToken, profile, cb) => {
            try {
                const email = profile.emails?.[0].value;

                if (!email) {
                    return cb(new Error('No email from Google'), false);
                }

                let user = await prisma.user.findUnique({ where: { email } });

                if (!user) {
                    user = await prisma.user.create({
                        data: {
                            email,
                            firstName: profile.displayName,
                            lastName: profile.name?.familyName ?? '',
                            username: 'random user',
                        },
                    });
                }

                cb(null, user);
            } catch (error) {
                cb(error, false);
            }
        }
    )
);

export default passport;

import passport from 'passport';

export const protect = passport.authenticate('accessToken', {
    session: false,
});

export const refreshProtect = passport.authenticate('refreshToken', {
    session: false,
});

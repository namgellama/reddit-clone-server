import nodemailer from 'nodemailer';

import { config } from '.';

export const transporter = nodemailer.createTransport({
    host: 'smtp.gmail.com',
    port: 587,
    secure: false,
    auth: {
        user: config.nodemailer.email,
        pass: config.nodemailer.password,
    },
});

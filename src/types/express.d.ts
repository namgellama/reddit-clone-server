export interface AuthUser {
    id: string;
    email: string;
    username: string;
    createdAt: Date;
    updatedAt: Date;
}

declare global {
    namespace Express {
        interface User extends AuthUser {}
    }
}

export {};

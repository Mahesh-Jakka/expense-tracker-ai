export type Role = 'admin' | 'employee';

export interface User {
  id: string;
  username: string;
  passwordHash: string;
  role: Role;
}

export interface AuthUser {
  id: string;
  username: string;
  role: Role;
}

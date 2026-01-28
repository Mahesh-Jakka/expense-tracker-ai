import { User, AuthUser } from '@/types/auth';

const USERS_KEY = 'expense-tracker-users';
const SESSION_KEY = 'expense-tracker-session';

function simpleHash(password: string): string {
  let hash = 0;
  for (let i = 0; i < password.length; i++) {
    const char = password.charCodeAt(i);
    hash = ((hash << 5) - hash) + char;
    hash |= 0;
  }
  return 'h_' + Math.abs(hash).toString(36);
}

function getUsers(): User[] {
  if (typeof window === 'undefined') return [];
  try {
    const data = localStorage.getItem(USERS_KEY);
    if (!data) return [];
    return JSON.parse(data);
  } catch {
    return [];
  }
}

function saveUsers(users: User[]): void {
  if (typeof window === 'undefined') return;
  localStorage.setItem(USERS_KEY, JSON.stringify(users));
}

export function seedAdmin(): void {
  const users = getUsers();
  if (users.some((u) => u.username === 'admin')) return;
  users.push({
    id: 'admin-001',
    username: 'admin',
    passwordHash: simpleHash('admin123'),
    role: 'admin',
  });
  saveUsers(users);
}

export function signup(username: string, password: string): AuthUser | string {
  const users = getUsers();
  if (users.some((u) => u.username === username)) {
    return 'Username already exists';
  }
  const newUser: User = {
    id: crypto.randomUUID ? crypto.randomUUID() : Date.now().toString(36),
    username,
    passwordHash: simpleHash(password),
    role: 'employee',
  };
  users.push(newUser);
  saveUsers(users);
  const authUser: AuthUser = { id: newUser.id, username: newUser.username, role: newUser.role };
  setSession(authUser);
  return authUser;
}

export function login(username: string, password: string): AuthUser | string {
  seedAdmin();
  const users = getUsers();
  const user = users.find((u) => u.username === username);
  if (!user) return 'Invalid username or password';
  if (user.passwordHash !== simpleHash(password)) return 'Invalid username or password';
  const authUser: AuthUser = { id: user.id, username: user.username, role: user.role };
  setSession(authUser);
  return authUser;
}

export function setSession(user: AuthUser): void {
  if (typeof window === 'undefined') return;
  localStorage.setItem(SESSION_KEY, JSON.stringify(user));
}

export function getSession(): AuthUser | null {
  if (typeof window === 'undefined') return null;
  try {
    const data = localStorage.getItem(SESSION_KEY);
    if (!data) return null;
    return JSON.parse(data);
  } catch {
    return null;
  }
}

export function clearSession(): void {
  if (typeof window === 'undefined') return;
  localStorage.removeItem(SESSION_KEY);
}

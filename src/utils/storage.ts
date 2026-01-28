import { Expense } from '@/types';

const STORAGE_KEY = 'expense-tracker-expenses';

export function getExpenses(): Expense[] {
  if (typeof window === 'undefined') return [];

  try {
    const data = localStorage.getItem(STORAGE_KEY);
    if (!data) return [];
    return JSON.parse(data);
  } catch {
    console.error('Failed to parse expenses from localStorage');
    return [];
  }
}

export function saveExpenses(expenses: Expense[]): void {
  if (typeof window === 'undefined') return;

  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(expenses));
  } catch {
    console.error('Failed to save expenses to localStorage');
  }
}

export function addExpense(expense: Expense): Expense[] {
  const expenses = getExpenses();
  const updated = [expense, ...expenses];
  saveExpenses(updated);
  return updated;
}

export function updateExpense(id: string, updates: Partial<Expense>): Expense[] {
  const expenses = getExpenses();
  const updated = expenses.map((expense) =>
    expense.id === id
      ? { ...expense, ...updates, updatedAt: new Date().toISOString() }
      : expense
  );
  saveExpenses(updated);
  return updated;
}

export function deleteExpense(id: string): Expense[] {
  const expenses = getExpenses();
  const updated = expenses.filter((expense) => expense.id !== id);
  saveExpenses(updated);
  return updated;
}

export function getExpensesByUser(userId: string): Expense[] {
  return getExpenses().filter((e) => e.submittedBy === userId);
}

export function clearAllExpenses(): void {
  if (typeof window === 'undefined') return;
  localStorage.removeItem(STORAGE_KEY);
}

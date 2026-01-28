'use client';

import React, { createContext, useContext, useState, useEffect, useCallback } from 'react';
import { v4 as uuidv4 } from 'uuid';
import { Expense, ExpenseFormData, Category, CATEGORY_COLORS } from '@/types';
import {
  getExpenses,
  saveExpenses,
} from '@/utils/storage';
import { getCurrentDateString, getMonthStart, getMonthEnd } from '@/utils/format';
import { useAuth } from '@/context/AuthContext';

interface ExpenseContextType {
  expenses: Expense[];
  isLoading: boolean;
  addExpense: (data: ExpenseFormData) => void;
  updateExpense: (id: string, data: ExpenseFormData) => void;
  deleteExpense: (id: string) => void;
  getExpenseById: (id: string) => Expense | undefined;
  getTotalSpending: () => number;
  getMonthlySpending: () => number;
  getCategorySpending: () => { name: Category; value: number; color: string }[];
  getMonthlyTrend: () => { month: string; amount: number }[];
  getFilteredExpenses: (
    startDate?: string,
    endDate?: string,
    category?: Category | 'All',
    searchQuery?: string
  ) => Expense[];
  approveExpense: (id: string) => void;
  rejectExpense: (id: string) => void;
}

const ExpenseContext = createContext<ExpenseContextType | undefined>(undefined);

export function ExpenseProvider({ children }: { children: React.ReactNode }) {
  const [allExpenses, setAllExpenses] = useState<Expense[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const { user } = useAuth();

  useEffect(() => {
    const stored = getExpenses();
    setAllExpenses(stored);
    setIsLoading(false);
  }, []);

  // For employees, filter to their own expenses. For admin, show all.
  const expenses = user?.role === 'admin'
    ? allExpenses
    : allExpenses.filter((e) => e.submittedBy === user?.id);

  const addExpense = useCallback((data: ExpenseFormData) => {
    if (!user) return;
    const newExpense: Expense = {
      id: uuidv4(),
      amount: parseFloat(data.amount),
      description: data.description.trim(),
      category: data.category,
      date: data.date || getCurrentDateString(),
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
      paymentMethod: data.paymentMethod,
      status: data.paymentMethod === 'company_card' ? 'approved' : 'pending',
      submittedBy: user.id,
      submittedByName: user.username,
    };

    setAllExpenses((prev) => {
      const updated = [newExpense, ...prev];
      saveExpenses(updated);
      return updated;
    });
  }, [user]);

  const updateExpense = useCallback((id: string, data: ExpenseFormData) => {
    setAllExpenses((prev) => {
      const updated = prev.map((expense) =>
        expense.id === id
          ? {
              ...expense,
              amount: parseFloat(data.amount),
              description: data.description.trim(),
              category: data.category,
              date: data.date,
              paymentMethod: data.paymentMethod,
              status: data.paymentMethod === 'company_card' ? 'approved' as const : expense.status,
              updatedAt: new Date().toISOString(),
            }
          : expense
      );
      saveExpenses(updated);
      return updated;
    });
  }, []);

  const deleteExpense = useCallback((id: string) => {
    setAllExpenses((prev) => {
      const updated = prev.filter((expense) => expense.id !== id);
      saveExpenses(updated);
      return updated;
    });
  }, []);

  const approveExpense = useCallback((id: string) => {
    setAllExpenses((prev) => {
      const updated = prev.map((expense) =>
        expense.id === id ? { ...expense, status: 'approved' as const, updatedAt: new Date().toISOString() } : expense
      );
      saveExpenses(updated);
      return updated;
    });
  }, []);

  const rejectExpense = useCallback((id: string) => {
    setAllExpenses((prev) => {
      const updated = prev.map((expense) =>
        expense.id === id ? { ...expense, status: 'rejected' as const, updatedAt: new Date().toISOString() } : expense
      );
      saveExpenses(updated);
      return updated;
    });
  }, []);

  const getExpenseById = useCallback(
    (id: string) => {
      return expenses.find((expense) => expense.id === id);
    },
    [expenses]
  );

  const getTotalSpending = useCallback(() => {
    return expenses.reduce((sum, expense) => sum + expense.amount, 0);
  }, [expenses]);

  const getMonthlySpending = useCallback(() => {
    const monthStart = getMonthStart();
    const monthEnd = getMonthEnd();

    return expenses
      .filter((expense) => expense.date >= monthStart && expense.date <= monthEnd)
      .reduce((sum, expense) => sum + expense.amount, 0);
  }, [expenses]);

  const getCategorySpending = useCallback(() => {
    const categoryMap = new Map<Category, number>();

    expenses.forEach((expense) => {
      const current = categoryMap.get(expense.category) || 0;
      categoryMap.set(expense.category, current + expense.amount);
    });

    return Array.from(categoryMap.entries())
      .map(([name, value]) => ({
        name,
        value,
        color: CATEGORY_COLORS[name],
      }))
      .sort((a, b) => b.value - a.value);
  }, [expenses]);

  const getMonthlyTrend = useCallback(() => {
    const monthMap = new Map<string, number>();

    expenses.forEach((expense) => {
      const monthKey = expense.date.substring(0, 7);
      const current = monthMap.get(monthKey) || 0;
      monthMap.set(monthKey, current + expense.amount);
    });

    return Array.from(monthMap.entries())
      .map(([month, amount]) => ({ month, amount }))
      .sort((a, b) => a.month.localeCompare(b.month))
      .slice(-6);
  }, [expenses]);

  const getFilteredExpenses = useCallback(
    (
      startDate?: string,
      endDate?: string,
      category?: Category | 'All',
      searchQuery?: string
    ) => {
      return expenses.filter((expense) => {
        if (startDate && expense.date < startDate) return false;
        if (endDate && expense.date > endDate) return false;
        if (category && category !== 'All' && expense.category !== category)
          return false;
        if (searchQuery) {
          const query = searchQuery.toLowerCase();
          if (
            !expense.description.toLowerCase().includes(query) &&
            !expense.category.toLowerCase().includes(query)
          ) {
            return false;
          }
        }
        return true;
      });
    },
    [expenses]
  );

  const value = {
    expenses,
    isLoading,
    addExpense,
    updateExpense,
    deleteExpense,
    getExpenseById,
    getTotalSpending,
    getMonthlySpending,
    getCategorySpending,
    getMonthlyTrend,
    getFilteredExpenses,
    approveExpense,
    rejectExpense,
  };

  return (
    <ExpenseContext.Provider value={value}>{children}</ExpenseContext.Provider>
  );
}

export function useExpenses() {
  const context = useContext(ExpenseContext);
  if (context === undefined) {
    throw new Error('useExpenses must be used within an ExpenseProvider');
  }
  return context;
}

'use client';

import React from 'react';
import Link from 'next/link';
import { useExpenses } from '@/context/ExpenseContext';
import { formatCurrency, formatDate } from '@/utils/format';
import { CATEGORY_ICONS, CATEGORY_COLORS } from '@/types';

export default function RecentExpenses() {
  const { expenses, isLoading } = useExpenses();

  if (isLoading) {
    return (
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <div className="h-5 bg-gray-200 rounded w-1/3 mb-6 animate-pulse"></div>
        {[...Array(5)].map((_, i) => (
          <div key={i} className="flex items-center gap-4 py-3 animate-pulse">
            <div className="w-10 h-10 bg-gray-200 rounded-lg"></div>
            <div className="flex-1">
              <div className="h-4 bg-gray-200 rounded w-1/2 mb-2"></div>
              <div className="h-3 bg-gray-100 rounded w-1/3"></div>
            </div>
            <div className="h-5 bg-gray-200 rounded w-16"></div>
          </div>
        ))}
      </div>
    );
  }

  const recentExpenses = expenses.slice(0, 5);

  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-semibold text-gray-900">Recent Expenses</h3>
        <Link
          href="/expenses"
          className="text-sm font-medium text-emerald-600 hover:text-emerald-700"
        >
          View All
        </Link>
      </div>

      {recentExpenses.length === 0 ? (
        <div className="py-8 text-center">
          <div className="w-12 h-12 mx-auto mb-3 bg-gray-100 rounded-full flex items-center justify-center">
            <svg
              className="w-6 h-6 text-gray-400"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M12 6v6m0 0v6m0-6h6m-6 0H6"
              />
            </svg>
          </div>
          <p className="text-gray-500 mb-3">No expenses yet</p>
          <Link
            href="/add"
            className="inline-flex items-center px-4 py-2 text-sm font-medium text-emerald-600 hover:text-emerald-700"
          >
            Add your first expense
          </Link>
        </div>
      ) : (
        <div className="divide-y divide-gray-100">
          {recentExpenses.map((expense) => (
            <div
              key={expense.id}
              className="flex items-center gap-4 py-3 first:pt-0 last:pb-0"
            >
              <div
                className="w-10 h-10 rounded-lg flex items-center justify-center text-lg"
                style={{ backgroundColor: `${CATEGORY_COLORS[expense.category]}15` }}
              >
                {CATEGORY_ICONS[expense.category]}
              </div>
              <div className="flex-1 min-w-0">
                <p className="font-medium text-gray-900 truncate">
                  {expense.description}
                </p>
                <p className="text-sm text-gray-500">{formatDate(expense.date)}</p>
              </div>
              <p className="font-semibold text-gray-900">
                {formatCurrency(expense.amount)}
              </p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

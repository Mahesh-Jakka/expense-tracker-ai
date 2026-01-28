'use client';

import React from 'react';
import { useExpenses } from '@/context/ExpenseContext';
import { formatCurrency } from '@/utils/format';

export default function DashboardCards() {
  const { expenses, getTotalSpending, getMonthlySpending, isLoading } =
    useExpenses();

  if (isLoading) {
    return (
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {[...Array(4)].map((_, i) => (
          <div
            key={i}
            className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 animate-pulse"
          >
            <div className="h-4 bg-gray-200 rounded w-1/2 mb-3"></div>
            <div className="h-8 bg-gray-200 rounded w-3/4"></div>
          </div>
        ))}
      </div>
    );
  }

  const totalSpending = getTotalSpending();
  const monthlySpending = getMonthlySpending();
  const pendingReimbursements = expenses.filter(
    (e) => e.paymentMethod === 'personal_card' && e.status === 'pending'
  );
  const approvedReimbursements = expenses.filter(
    (e) => e.paymentMethod === 'personal_card' && e.status === 'approved'
  );
  const pendingAmount = pendingReimbursements.reduce((s, e) => s + e.amount, 0);
  const approvedAmount = approvedReimbursements.reduce((s, e) => s + e.amount, 0);

  const cards = [
    {
      title: 'Total Spending',
      value: formatCurrency(totalSpending),
      icon: (
        <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
      ),
      bgColor: 'bg-emerald-50',
      textColor: 'text-emerald-600',
    },
    {
      title: 'This Month',
      value: formatCurrency(monthlySpending),
      icon: (
        <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
        </svg>
      ),
      bgColor: 'bg-blue-50',
      textColor: 'text-blue-600',
    },
    {
      title: 'Pending Reimbursement',
      value: formatCurrency(pendingAmount),
      subtitle: `${pendingReimbursements.length} expense${pendingReimbursements.length !== 1 ? 's' : ''} pending`,
      icon: (
        <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
      ),
      bgColor: 'bg-amber-50',
      textColor: 'text-amber-600',
    },
    {
      title: 'Approved Reimbursement',
      value: formatCurrency(approvedAmount),
      subtitle: `${approvedReimbursements.length} expense${approvedReimbursements.length !== 1 ? 's' : ''} approved`,
      icon: (
        <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
      ),
      bgColor: 'bg-purple-50',
      textColor: 'text-purple-600',
    },
  ];

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
      {cards.map((card, index) => (
        <div
          key={index}
          className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow"
        >
          <div className="flex items-center justify-between mb-4">
            <span className="text-sm font-medium text-gray-500">{card.title}</span>
            <div className={`p-2 rounded-lg ${card.bgColor}`}>
              <div className={card.textColor}>{card.icon}</div>
            </div>
          </div>
          <p className="text-2xl font-bold text-gray-900">{card.value}</p>
          {card.subtitle && (
            <p className="text-sm text-gray-500 mt-1">{card.subtitle}</p>
          )}
        </div>
      ))}
    </div>
  );
}

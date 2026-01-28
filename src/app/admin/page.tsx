'use client';

import React, { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/context/AuthContext';
import { useExpenses } from '@/context/ExpenseContext';
import { formatCurrency } from '@/utils/format';
import { getMonthStart, getMonthEnd } from '@/utils/format';
import { CategoryPieChart, MonthlyBarChart } from '@/components/Charts';
import AdminExpenseList from '@/components/AdminExpenseList';

export default function AdminPage() {
  const { user, isLoading } = useAuth();
  const router = useRouter();
  const { expenses } = useExpenses();

  useEffect(() => {
    if (!isLoading && (!user || user.role !== 'admin')) {
      router.replace('/login');
    }
  }, [user, isLoading, router]);

  if (isLoading || !user || user.role !== 'admin') {
    return (
      <div className="flex items-center justify-center py-12">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-emerald-600"></div>
      </div>
    );
  }

  const totalSpending = expenses.reduce((sum, e) => sum + e.amount, 0);
  const monthStart = getMonthStart();
  const monthEnd = getMonthEnd();
  const thisMonthSpending = expenses
    .filter((e) => e.date >= monthStart && e.date <= monthEnd)
    .reduce((sum, e) => sum + e.amount, 0);
  const pendingReimbursements = expenses.filter(
    (e) => e.status === 'pending' && e.paymentMethod === 'personal_card'
  ).length;
  const uniqueEmployees = new Set(expenses.map((e) => e.submittedBy)).size;

  const cards = [
    { label: 'Total Spending', value: formatCurrency(totalSpending), color: 'bg-emerald-50 text-emerald-700' },
    { label: 'This Month', value: formatCurrency(thisMonthSpending), color: 'bg-blue-50 text-blue-700' },
    { label: 'Pending Reimbursements', value: String(pendingReimbursements), color: 'bg-amber-50 text-amber-700' },
    { label: 'Employees', value: String(uniqueEmployees), color: 'bg-purple-50 text-purple-700' },
  ];

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Admin Dashboard</h1>
        <p className="text-gray-500 mt-1">Review and manage employee expense reimbursements</p>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        {cards.map((card) => (
          <div key={card.label} className="bg-white rounded-xl shadow-sm border border-gray-200 p-5">
            <p className="text-sm font-medium text-gray-500">{card.label}</p>
            <p className={`text-2xl font-bold mt-1 ${card.color.split(' ')[1]}`}>{card.value}</p>
          </div>
        ))}
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <CategoryPieChart />
        <MonthlyBarChart />
      </div>

      {/* Expense List */}
      <AdminExpenseList />
    </div>
  );
}

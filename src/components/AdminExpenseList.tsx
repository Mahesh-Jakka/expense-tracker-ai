'use client';

import React, { useState } from 'react';
import { useExpenses } from '@/context/ExpenseContext';
import { formatCurrency, formatDate } from '@/utils/format';
import { CATEGORY_ICONS, CATEGORY_COLORS } from '@/types';

export default function AdminExpenseList() {
  const { expenses, approveExpense, rejectExpense, isLoading } = useExpenses();
  const [viewReceiptUrl, setViewReceiptUrl] = useState<string | null>(null);

  if (isLoading) {
    return (
      <div className="flex items-center justify-center py-12">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-emerald-600"></div>
      </div>
    );
  }

  if (expenses.length === 0) {
    return (
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-12 text-center">
        <h3 className="text-lg font-medium text-gray-900 mb-2">No expenses submitted yet</h3>
        <p className="text-gray-500">Employee expenses will appear here.</p>
      </div>
    );
  }

  const pendingExpenses = expenses.filter((e) => e.status === 'pending');
  const otherExpenses = expenses.filter((e) => e.status !== 'pending');

  return (
    <div className="space-y-8">
      {pendingExpenses.length > 0 && (
        <div>
          <h2 className="text-lg font-semibold text-gray-900 mb-4">
            Pending Approval ({pendingExpenses.length})
          </h2>
          <div className="space-y-3">
            {pendingExpenses.map((expense) => (
              <div
                key={expense.id}
                className="bg-white rounded-xl shadow-sm border border-amber-200 p-4"
              >
                <div className="flex items-center gap-4">
                  <div
                    className="w-12 h-12 rounded-xl flex items-center justify-center text-2xl flex-shrink-0"
                    style={{ backgroundColor: `${CATEGORY_COLORS[expense.category]}15` }}
                  >
                    {CATEGORY_ICONS[expense.category]}
                  </div>
                  <div className="flex-1 min-w-0">
                    <h3 className="font-medium text-gray-900 truncate">{expense.description}</h3>
                    <div className="flex items-center gap-2 mt-1 flex-wrap">
                      <span className="text-sm text-gray-500">{expense.submittedByName}</span>
                      <span className="text-gray-300">|</span>
                      <span
                        className="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium"
                        style={{
                          backgroundColor: `${CATEGORY_COLORS[expense.category]}15`,
                          color: CATEGORY_COLORS[expense.category],
                        }}
                      >
                        {expense.category}
                      </span>
                      <span className="text-sm text-gray-500">{formatDate(expense.date)}</span>
                      <span className="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-orange-100 text-orange-700">
                        Personal Card
                      </span>
                    </div>
                  </div>
                  <div className="text-right flex-shrink-0">
                    <p className="text-lg font-semibold text-gray-900">{formatCurrency(expense.amount)}</p>
                  </div>
                  <div className="flex items-center gap-2 flex-shrink-0">
                    {expense.receiptUrl && (
                      <button
                        onClick={() => setViewReceiptUrl(expense.receiptUrl!)}
                        className="p-2 text-gray-400 hover:text-blue-600 hover:bg-blue-50 rounded-lg transition-colors"
                        title="View Receipt"
                      >
                        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15.172 7l-6.586 6.586a2 2 0 102.828 2.828l6.414-6.586a4 4 0 00-5.656-5.656l-6.415 6.585a6 6 0 108.486 8.486L20.5 13" />
                        </svg>
                      </button>
                    )}
                    <button
                      onClick={() => approveExpense(expense.id)}
                      className="px-3 py-1.5 text-sm font-medium text-white bg-emerald-600 hover:bg-emerald-700 rounded-lg transition-colors"
                    >
                      Approve
                    </button>
                    <button
                      onClick={() => rejectExpense(expense.id)}
                      className="px-3 py-1.5 text-sm font-medium text-white bg-red-600 hover:bg-red-700 rounded-lg transition-colors"
                    >
                      Reject
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      <div>
        <h2 className="text-lg font-semibold text-gray-900 mb-4">
          All Expenses ({expenses.length})
        </h2>
        <div className="space-y-3">
          {otherExpenses.concat(pendingExpenses).map((expense) => (
            <div
              key={expense.id}
              className="bg-white rounded-xl shadow-sm border border-gray-200 p-4"
            >
              <div className="flex items-center gap-4">
                <div
                  className="w-12 h-12 rounded-xl flex items-center justify-center text-2xl flex-shrink-0"
                  style={{ backgroundColor: `${CATEGORY_COLORS[expense.category]}15` }}
                >
                  {CATEGORY_ICONS[expense.category]}
                </div>
                <div className="flex-1 min-w-0">
                  <h3 className="font-medium text-gray-900 truncate">{expense.description}</h3>
                  <div className="flex items-center gap-2 mt-1 flex-wrap">
                    <span className="text-sm text-gray-500">{expense.submittedByName}</span>
                    <span className="text-gray-300">|</span>
                    <span
                      className="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium"
                      style={{
                        backgroundColor: `${CATEGORY_COLORS[expense.category]}15`,
                        color: CATEGORY_COLORS[expense.category],
                      }}
                    >
                      {expense.category}
                    </span>
                    <span className="text-sm text-gray-500">{formatDate(expense.date)}</span>
                    <span
                      className={`inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium ${
                        expense.paymentMethod === 'company_card'
                          ? 'bg-blue-100 text-blue-700'
                          : 'bg-orange-100 text-orange-700'
                      }`}
                    >
                      {expense.paymentMethod === 'company_card' ? 'Company Card' : 'Personal Card'}
                    </span>
                    <span
                      className={`inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium ${
                        expense.status === 'approved'
                          ? 'bg-emerald-100 text-emerald-700'
                          : expense.status === 'rejected'
                          ? 'bg-red-100 text-red-700'
                          : 'bg-amber-100 text-amber-700'
                      }`}
                    >
                      {expense.status.charAt(0).toUpperCase() + expense.status.slice(1)}
                    </span>
                  </div>
                </div>
                <div className="text-right flex-shrink-0">
                  <p className="text-lg font-semibold text-gray-900">{formatCurrency(expense.amount)}</p>
                </div>
                {expense.receiptUrl && (
                  <button
                    onClick={() => setViewReceiptUrl(expense.receiptUrl!)}
                    className="p-2 text-gray-400 hover:text-blue-600 hover:bg-blue-50 rounded-lg transition-colors flex-shrink-0"
                    title="View Receipt"
                  >
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15.172 7l-6.586 6.586a2 2 0 102.828 2.828l6.414-6.586a4 4 0 00-5.656-5.656l-6.415 6.585a6 6 0 108.486 8.486L20.5 13" />
                    </svg>
                  </button>
                )}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Receipt View Modal */}
      {viewReceiptUrl && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4" onClick={() => setViewReceiptUrl(null)}>
          <div className="bg-white rounded-xl shadow-xl max-w-2xl w-full p-6 max-h-[90vh] overflow-auto" onClick={(e) => e.stopPropagation()}>
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-semibold text-gray-900">Receipt</h3>
              <button onClick={() => setViewReceiptUrl(null)} className="p-1 text-gray-400 hover:text-gray-600 rounded">
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
            {viewReceiptUrl.startsWith('data:image') ? (
              <img src={viewReceiptUrl} alt="Receipt" className="w-full rounded-lg" />
            ) : (
              <iframe src={viewReceiptUrl} className="w-full h-[70vh] rounded-lg border" />
            )}
          </div>
        </div>
      )}
    </div>
  );
}

'use client';

import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useExpenses } from '@/context/ExpenseContext';
import { ExpenseFormData, CATEGORIES, CATEGORY_ICONS } from '@/types';
import { getCurrentDateString } from '@/utils/format';

interface ExpenseFormProps {
  editId?: string;
}

interface FormErrors {
  amount?: string;
  description?: string;
  date?: string;
}

export default function ExpenseForm({ editId }: ExpenseFormProps) {
  const router = useRouter();
  const { addExpense, updateExpense, getExpenseById } = useExpenses();
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [showSuccess, setShowSuccess] = useState(false);

  const [formData, setFormData] = useState<ExpenseFormData>({
    amount: '',
    description: '',
    category: 'Food',
    date: getCurrentDateString(),
    paymentMethod: 'company_card',
    receipt: '',
  });

  const [receiptPreview, setReceiptPreview] = useState<string | null>(null);
  const [errors, setErrors] = useState<FormErrors>({});

  useEffect(() => {
    if (editId) {
      const expense = getExpenseById(editId);
      if (expense) {
        setFormData({
          amount: expense.amount.toString(),
          description: expense.description,
          category: expense.category,
          date: expense.date,
          paymentMethod: expense.paymentMethod,
          receipt: '',
        });
        if (expense.receiptUrl) {
          setReceiptPreview(expense.receiptUrl);
        }
      }
    }
  }, [editId, getExpenseById]);

  const validateForm = (): boolean => {
    const newErrors: FormErrors = {};

    const amount = parseFloat(formData.amount);
    if (!formData.amount || isNaN(amount)) {
      newErrors.amount = 'Amount is required';
    } else if (amount <= 0) {
      newErrors.amount = 'Amount must be greater than 0';
    } else if (amount > 1000000) {
      newErrors.amount = 'Amount is too large';
    }

    if (!formData.description.trim()) {
      newErrors.description = 'Description is required';
    } else if (formData.description.trim().length < 2) {
      newErrors.description = 'Description is too short';
    } else if (formData.description.trim().length > 200) {
      newErrors.description = 'Description is too long (max 200 characters)';
    }

    if (!formData.date) {
      newErrors.date = 'Date is required';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!validateForm()) return;

    setIsSubmitting(true);

    await new Promise((resolve) => setTimeout(resolve, 300));

    if (editId) {
      updateExpense(editId, formData);
    } else {
      addExpense(formData);
    }

    setShowSuccess(true);
    setIsSubmitting(false);

    setTimeout(() => {
      if (editId) {
        router.push('/expenses');
      } else {
        setFormData({
          amount: '',
          description: '',
          category: 'Food',
          date: getCurrentDateString(),
          paymentMethod: 'company_card',
          receipt: '',
        });
        setReceiptPreview(null);
        setShowSuccess(false);
      }
    }, 1000);
  };

  const handleReceiptChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;
    if (file.size > 5 * 1024 * 1024) {
      alert('File must be under 5MB');
      return;
    }
    const reader = new FileReader();
    reader.onload = () => {
      const result = reader.result as string;
      setReceiptPreview(result);
      setFormData((prev) => ({ ...prev, receipt: result }));
    };
    reader.readAsDataURL(file);
  };

  const handleAmountChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    if (/^\d*\.?\d{0,2}$/.test(value) || value === '') {
      setFormData({ ...formData, amount: value });
      if (errors.amount) setErrors({ ...errors, amount: undefined });
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      {/* Success Message */}
      {showSuccess && (
        <div className="bg-emerald-50 border border-emerald-200 rounded-lg p-4 flex items-center space-x-3">
          <div className="flex-shrink-0">
            <svg
              className="w-5 h-5 text-emerald-500"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M5 13l4 4L19 7"
              />
            </svg>
          </div>
          <p className="text-emerald-700 font-medium">
            {editId ? 'Expense updated successfully!' : 'Expense added successfully!'}
          </p>
        </div>
      )}

      {/* Amount Field */}
      <div>
        <label
          htmlFor="amount"
          className="block text-sm font-medium text-gray-700 mb-2"
        >
          Amount
        </label>
        <div className="relative">
          <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
            <span className="text-gray-500 text-lg">$</span>
          </div>
          <input
            type="text"
            id="amount"
            inputMode="decimal"
            placeholder="0.00"
            value={formData.amount}
            onChange={handleAmountChange}
            className={`block w-full pl-8 pr-4 py-3 text-lg border rounded-lg focus:outline-none focus:ring-2 transition-colors ${
              errors.amount
                ? 'border-red-300 focus:ring-red-500 focus:border-red-500'
                : 'border-gray-300 focus:ring-emerald-500 focus:border-emerald-500'
            }`}
          />
        </div>
        {errors.amount && (
          <p className="mt-2 text-sm text-red-600">{errors.amount}</p>
        )}
      </div>

      {/* Description Field */}
      <div>
        <label
          htmlFor="description"
          className="block text-sm font-medium text-gray-700 mb-2"
        >
          Description
        </label>
        <input
          type="text"
          id="description"
          placeholder="What was this expense for?"
          value={formData.description}
          onChange={(e) => {
            setFormData({ ...formData, description: e.target.value });
            if (errors.description) setErrors({ ...errors, description: undefined });
          }}
          className={`block w-full px-4 py-3 border rounded-lg focus:outline-none focus:ring-2 transition-colors ${
            errors.description
              ? 'border-red-300 focus:ring-red-500 focus:border-red-500'
              : 'border-gray-300 focus:ring-emerald-500 focus:border-emerald-500'
          }`}
        />
        {errors.description && (
          <p className="mt-2 text-sm text-red-600">{errors.description}</p>
        )}
      </div>

      {/* Category Field */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Category
        </label>
        <div className="grid grid-cols-2 sm:grid-cols-3 gap-3">
          {CATEGORIES.map((category) => (
            <button
              key={category}
              type="button"
              onClick={() => setFormData({ ...formData, category })}
              className={`flex items-center justify-center space-x-2 px-4 py-3 rounded-lg border-2 transition-all ${
                formData.category === category
                  ? 'border-emerald-500 bg-emerald-50 text-emerald-700'
                  : 'border-gray-200 hover:border-gray-300 text-gray-700'
              }`}
            >
              <span className="text-xl">{CATEGORY_ICONS[category]}</span>
              <span className="font-medium">{category}</span>
            </button>
          ))}
        </div>
      </div>

      {/* Payment Method Field */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Payment Method
        </label>
        <div className="grid grid-cols-2 gap-3">
          <button
            type="button"
            onClick={() => setFormData({ ...formData, paymentMethod: 'company_card' })}
            className={`flex items-center justify-center space-x-2 px-4 py-3 rounded-lg border-2 transition-all ${
              formData.paymentMethod === 'company_card'
                ? 'border-blue-500 bg-blue-50 text-blue-700'
                : 'border-gray-200 hover:border-gray-300 text-gray-700'
            }`}
          >
            <span className="font-medium">Company Card</span>
          </button>
          <button
            type="button"
            onClick={() => setFormData({ ...formData, paymentMethod: 'personal_card' })}
            className={`flex items-center justify-center space-x-2 px-4 py-3 rounded-lg border-2 transition-all ${
              formData.paymentMethod === 'personal_card'
                ? 'border-orange-500 bg-orange-50 text-orange-700'
                : 'border-gray-200 hover:border-gray-300 text-gray-700'
            }`}
          >
            <span className="font-medium">Personal Card</span>
          </button>
        </div>
        {formData.paymentMethod === 'company_card' && (
          <p className="mt-2 text-sm text-blue-600">No reimbursement needed</p>
        )}
        {formData.paymentMethod === 'personal_card' && (
          <p className="mt-2 text-sm text-orange-600">Will require admin approval for reimbursement</p>
        )}
      </div>

      {/* Date Field */}
      <div>
        <label
          htmlFor="date"
          className="block text-sm font-medium text-gray-700 mb-2"
        >
          Date
        </label>
        <input
          type="date"
          id="date"
          value={formData.date}
          onChange={(e) => {
            setFormData({ ...formData, date: e.target.value });
            if (errors.date) setErrors({ ...errors, date: undefined });
          }}
          className={`block w-full px-4 py-3 border rounded-lg focus:outline-none focus:ring-2 transition-colors ${
            errors.date
              ? 'border-red-300 focus:ring-red-500 focus:border-red-500'
              : 'border-gray-300 focus:ring-emerald-500 focus:border-emerald-500'
          }`}
        />
        {errors.date && (
          <p className="mt-2 text-sm text-red-600">{errors.date}</p>
        )}
      </div>

      {/* Receipt Upload */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Receipt (optional)
        </label>
        <input
          type="file"
          accept="image/*,application/pdf"
          onChange={handleReceiptChange}
          className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-medium file:bg-emerald-50 file:text-emerald-700 hover:file:bg-emerald-100"
        />
        {receiptPreview && (
          <div className="mt-3">
            {receiptPreview.startsWith('data:image') ? (
              <img
                src={receiptPreview}
                alt="Receipt preview"
                className="max-h-40 rounded-lg border border-gray-200"
              />
            ) : (
              <div className="flex items-center gap-2 text-sm text-gray-600">
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
                PDF receipt attached
              </div>
            )}
            <button
              type="button"
              onClick={() => {
                setReceiptPreview(null);
                setFormData((prev) => ({ ...prev, receipt: '' }));
              }}
              className="mt-2 text-sm text-red-600 hover:text-red-700"
            >
              Remove receipt
            </button>
          </div>
        )}
      </div>

      {/* Submit Button */}
      <button
        type="submit"
        disabled={isSubmitting}
        className="w-full py-3 px-4 bg-emerald-600 hover:bg-emerald-700 disabled:bg-emerald-400 text-white font-medium rounded-lg transition-colors flex items-center justify-center space-x-2"
      >
        {isSubmitting ? (
          <>
            <svg
              className="animate-spin h-5 w-5 text-white"
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
            >
              <circle
                className="opacity-25"
                cx="12"
                cy="12"
                r="10"
                stroke="currentColor"
                strokeWidth="4"
              ></circle>
              <path
                className="opacity-75"
                fill="currentColor"
                d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
              ></path>
            </svg>
            <span>Saving...</span>
          </>
        ) : (
          <span>{editId ? 'Update Expense' : 'Add Expense'}</span>
        )}
      </button>
    </form>
  );
}

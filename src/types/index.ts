export type Category =
  | 'Food'
  | 'Transportation'
  | 'Entertainment'
  | 'Shopping'
  | 'Bills'
  | 'Other';

export type PaymentMethod = 'company_card' | 'personal_card';
export type ExpenseStatus = 'pending' | 'approved' | 'rejected';

export interface Expense {
  id: string;
  amount: number;
  description: string;
  category: Category;
  date: string; // ISO date string
  createdAt: string;
  updatedAt: string;
  paymentMethod: PaymentMethod;
  status: ExpenseStatus;
  submittedBy: string;
  submittedByName: string;
}

export interface ExpenseFormData {
  amount: string;
  description: string;
  category: Category;
  date: string;
  paymentMethod: PaymentMethod;
}

export interface ExpenseFilters {
  startDate: string;
  endDate: string;
  category: Category | 'All';
  searchQuery: string;
}

export interface CategoryData {
  name: Category;
  value: number;
  color: string;
}

export interface MonthlyData {
  month: string;
  amount: number;
}

export const CATEGORIES: Category[] = [
  'Food',
  'Transportation',
  'Entertainment',
  'Shopping',
  'Bills',
  'Other',
];

export const CATEGORY_COLORS: Record<Category, string> = {
  Food: '#10B981',
  Transportation: '#3B82F6',
  Entertainment: '#8B5CF6',
  Shopping: '#F59E0B',
  Bills: '#EF4444',
  Other: '#6B7280',
};

export const CATEGORY_ICONS: Record<Category, string> = {
  Food: '🍔',
  Transportation: '🚗',
  Entertainment: '🎬',
  Shopping: '🛒',
  Bills: '📄',
  Other: '📦',
};

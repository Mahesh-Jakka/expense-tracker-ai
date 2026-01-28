import { format, parseISO, isValid } from 'date-fns';

export function formatCurrency(amount: number): string {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  }).format(amount);
}

export function formatDate(dateString: string): string {
  try {
    const date = parseISO(dateString);
    if (!isValid(date)) return dateString;
    return format(date, 'MMM d, yyyy');
  } catch {
    return dateString;
  }
}

export function formatDateForInput(dateString: string): string {
  try {
    const date = parseISO(dateString);
    if (!isValid(date)) return '';
    return format(date, 'yyyy-MM-dd');
  } catch {
    return '';
  }
}

export function formatMonthYear(dateString: string): string {
  try {
    const date = parseISO(dateString);
    if (!isValid(date)) return dateString;
    return format(date, 'MMM yyyy');
  } catch {
    return dateString;
  }
}

export function getCurrentDateString(): string {
  return format(new Date(), 'yyyy-MM-dd');
}

export function getMonthStart(date: Date = new Date()): string {
  return format(new Date(date.getFullYear(), date.getMonth(), 1), 'yyyy-MM-dd');
}

export function getMonthEnd(date: Date = new Date()): string {
  return format(
    new Date(date.getFullYear(), date.getMonth() + 1, 0),
    'yyyy-MM-dd'
  );
}

export function parseCurrency(value: string): number {
  const cleaned = value.replace(/[^0-9.-]+/g, '');
  const parsed = parseFloat(cleaned);
  return isNaN(parsed) ? 0 : parsed;
}

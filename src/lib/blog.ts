// Shared helpers for the repo-based blog.

export function formatPostDate(date: Date): string {
  return date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  });
}

export function readTimeInMinutes(body: string | undefined): number {
  const text = body ?? '';
  const words = text.replace(/<[^>]+>/g, ' ').split(/\s+/).filter(Boolean).length;
  return Math.max(1, Math.round(words / 200));
}

// frontend_ui/src/api/auth.js

export function getAuthHeaders() {
  const token = localStorage.getItem('clerkToken'); // or use Clerk SDK
  return {
    Authorization: `Bearer ${token}`,
    'Content-Type': 'application/json',
  };
}

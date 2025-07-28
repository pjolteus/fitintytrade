import { useEffect, useState } from 'react';
import toast from 'react-hot-toast';

const useTheme = () => {
  const [isDark, setIsDark] = useState(() => {
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme) return savedTheme === 'dark';
    return window.matchMedia('(prefers-color-scheme: dark)').matches;
  });

  useEffect(() => {
    const root = document.documentElement;
    root.classList.toggle('dark', isDark);
    localStorage.setItem('theme', isDark ? 'dark' : 'light');
  }, [isDark]);

  const toggleTheme = () => {
    setIsDark(prev => {
      const newTheme = !prev;
      toast.success(newTheme ? '🌙 Dark mode enabled' : '☀️ Light mode enabled');
      return newTheme;
    });
  };

  return { isDark, toggleTheme };
};

export default useTheme;

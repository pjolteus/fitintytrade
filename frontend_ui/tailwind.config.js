export default {
  content: ['./index.html', './src/**/*.{js,jsx}'],
  darkMode: 'class', // Enables class-based dark mode (via "dark" class on <html>)
  theme: {
    extend: {
      colors: {
        gold: '#B8860B',
      },
      animation: {
        'spin-slow': 'spin 2s linear infinite',
      },
    },
  },
  plugins: [],
};

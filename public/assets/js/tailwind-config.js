/* Shared Tailwind (CDN) configuration for mogrov.com.
   Loaded on every page AFTER the Tailwind CDN script. */
tailwind.config = {
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        // Dark theme — Tokyo Night identity
        tokyo: {
          bg: '#1a1b26',
          surface: '#24283b',
          ink: '#16161e',
          blue: '#7aa2f7',
          cyan: '#7dcfff',
          purple: '#bb9af7',
          green: '#9ece6a',
          red: '#f7768e',
          orange: '#e0af68',
          comment: '#565f89',
        },
        // Light theme — refined "engineering paper"
        brand: {
          blue: '#2e5cff',
          ink: '#16161e',
          paper: '#f7f8fb',
          amber: '#f0a500',
        },
      },
      fontFamily: {
        display: ['"Geist"', 'system-ui', 'sans-serif'],
        sans: ['"Geist"', 'system-ui', 'sans-serif'],
        mono: ['"Geist Mono"', 'ui-monospace', 'monospace'],
      },
      animation: {
        float: 'float 6s ease-in-out infinite',
        'pulse-slow': 'pulse 4s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        shimmer: 'shimmer 4s linear infinite',
      },
      keyframes: {
        float: {
          '0%, 100%': { transform: 'translateY(0)' },
          '50%': { transform: 'translateY(-10px)' },
        },
        shimmer: {
          '0%': { backgroundPosition: '-200% 0' },
          '100%': { backgroundPosition: '200% 0' },
        },
      },
    },
  },
};

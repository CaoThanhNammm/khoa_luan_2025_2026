/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'charcoal': '#111827',
        'lavender': '#d6ccf2',
        'sky-blue': '#c3e0f0',
        'off-white': '#fefbff',
        'beige': '#f6f3eb',
      },
      fontFamily: {
        'heading': ['Playfair Display', 'serif'],
        'body': ['Inter', 'Lato', 'sans-serif'],
        'claude': ['-apple-system', 'BlinkMacSystemFont', 'Inter', 'Source Sans Pro', 'Segoe UI', 'system-ui', 'sans-serif'],
        'claude-display': ['-apple-system', 'BlinkMacSystemFont', 'Inter', 'Source Sans Pro', 'Segoe UI', 'system-ui', 'sans-serif'],
        'claude-body': ['-apple-system', 'BlinkMacSystemFont', 'Inter', 'Source Sans Pro', 'Segoe UI', 'system-ui', 'sans-serif'],
        'mono-modern': ['JetBrains Mono', 'Fira Code', 'SF Mono', 'Consolas', 'monospace'],
      },
    },
  },
  plugins: [],
}


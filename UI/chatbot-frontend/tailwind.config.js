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
      },
    },
  },
  plugins: [],
}


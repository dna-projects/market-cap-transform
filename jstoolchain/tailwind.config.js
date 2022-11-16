/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["../templates/**/*.{html,js}"],
  theme: {
    extend: {
      colors: {
        'border-blue': '#1E00D9',
      },
      // dropShadow: {
      //   'turquoise': '0 80px 100px rgba(41, 144, 176, 0.8)',
      // }
    },
  },
  plugins: [],
}

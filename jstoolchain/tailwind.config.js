/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["../templates/**/*.{html,js}"],
  theme: {
    extend: {
      colors: {
        'red-test': '#FF4B32',
      },
    },
  },
  plugins: [],
}

/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/**/*.{html,ts}', // Asegúrate de incluir las extensiones que Tailwind debe analizar
  ],
  theme: {
    extend: {
      colors: {
        '[#2c3e50]': '#2c3e50',
        '[#34495e]': '#34495e',
      },
    },
  },
  plugins: [],
}

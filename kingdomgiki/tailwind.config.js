/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html", // Adjust this based on your templates' location
    "./static/**/*.js", // Adjust this based on your static files' location
    "./static/**/*.css", // Ensure Tailwind can process your CSS files
  ],
  theme: {
    extend: {},
  },
  plugins: [],
};

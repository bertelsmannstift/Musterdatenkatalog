module.exports = {
  content: [
  "./layouts/**/*.html",
  "./content/**/*.{html,js}"
  ],
  theme: {
    extend: {},
  },
  plugins: [
    require('@tailwindcss/typography'),
  ],
}

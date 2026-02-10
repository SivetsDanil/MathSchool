/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./templates/**/*.html"],
  safelist: [
    'section-title',
    'heading-block',
    'text-body',
    'feature-card',
    'btn-primary'
  ],
  darkMode: 'class', // ← включает поддержку class="dark"
  theme: {
    extend: {
      colors: {
        // Твоя палитра
        school: {
          primary: '#1e40af',
          secondary: '#059669',
          accent: '#7c3aed',
        }
      },
      // Семантические стили текста
      typography: {
        DEFAULT: {
          css: {
            '--tw-prose-body': '#374151',     // text-gray-700
            '--tw-prose-headings': '#111827', // text-gray-900
            '--tw-prose-links': '#1e40af',    // school.primary
          }
        }
      }
    },
  },
  plugins: [],
}
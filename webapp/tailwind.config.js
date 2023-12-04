/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{html,js,svelte,ts}'],
  theme: {
    extend: {}
  },
  plugins: [
    require("daisyui"),
  ],
  corePlugins: {
    // ...
   scrollBehavior: true,
  },
  darkMode: ['class', '[data-theme="dark"]'],
  daisyui: {
    themes: [
      {
        light: {
          ...require("daisyui/src/theming/themes")["light"],
          primary: "#334155",
        }
      },
      {
        dark: {
          ...require("daisyui/src/theming/themes")["dark"],
          primary: "#94a3b8",
        }
      },
    ]
  }
};

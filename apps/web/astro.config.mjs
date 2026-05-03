import { defineConfig } from "astro/config";

export default defineConfig({
  site: "https://aifund.pages.dev",
  vite: {
    resolve: {
      preserveSymlinks: true,
    },
    optimizeDeps: {
      include: ["sqlprism"],
    },
  },
});

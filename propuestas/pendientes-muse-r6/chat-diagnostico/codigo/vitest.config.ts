import { defineConfig } from 'vitest/config';

export default defineConfig({
  // Cache dentro de esta carpeta: no se escribe nada fuera de codigo/.
  cacheDir: './.vitest-cache',
  test: {
    include: ['tests/**/*.test.ts'],
  },
});

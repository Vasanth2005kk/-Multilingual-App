// vite.config.js
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    host: '0.0.0.0',     // 👈 Expose to network (not just localhost)
    port: 9000,           // 👈 Same port as before
    strictPort: true,     // 👈 Prevent automatic port switching
    proxy: {
      '/api': {
        target: 'http://localhost:5000', // Flask backend
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, '/api'),
      },
    },
  },
})

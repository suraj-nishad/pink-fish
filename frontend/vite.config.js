import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    // Allow Railway preview host and local dev hosts to bypass host header blocking.
    // Using explicit list for dev; can be switched to 'all' if broader access needed.
    allowedHosts: [
      'localhost',
      '127.0.0.1',
      'pink-fish-ui.up.railway.app',
      // Match any Railway generated subdomain (subdomain.railway.app)
      '.railway.app'
    ],
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
      '/health': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      }
    }
  },
  preview: {
    host: '0.0.0.0',
    strictPort: false,
    // Explicit list of hosts permitted in preview (Railway + local dev).
    // Avoid using broad 'all' for tighter control.
    allowedHosts: [
      'pink-fish-ui.up.railway.app', // deployed UI domain
      'localhost',
      '127.0.0.1'
    ],
    // Ensure the preview server binds to the PORT Railway provides if not passed via CLI.
    port: parseInt(process.env.PORT || '8080', 10),
    proxy: {
      '/api': {
        target: process.env.VITE_API_URL || 'http://localhost:8000',
        changeOrigin: true,
      },
      '/health': {
        target: process.env.VITE_API_URL || 'http://localhost:8000',
        changeOrigin: true,
      }
    }
  },
  build: {
    outDir: 'dist',
    sourcemap: false,
    rollupOptions: {
      output: {
        manualChunks: {
          'react-vendor': ['react', 'react-dom', 'react-router-dom'],
          'carbon': ['@carbon/react', '@carbon/icons-react'],
          'charts': ['recharts'],
        },
      },
    },
  },
})

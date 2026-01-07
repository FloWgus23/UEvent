import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src')
    }
  },
  server: {
    host: '0.0.0.0',
    port: Number(process.env.PORT) || 5173
  },
  preview: {
    host: '0.0.0.0',
    port: Number(process.env.PORT) || 8080
  }
})
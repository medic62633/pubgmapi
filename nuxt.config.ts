// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  devtools: { enabled: true },
  modules: ['@nuxtjs/tailwindcss'],
  css: ['~/assets/css/main.css'],
  app: {
    head: {
      title: 'PUBG Mobile User ID Checker',
      meta: [
        { charset: 'utf-8' },
        { name: 'viewport', content: 'width=device-width, initial-scale=1' },
        { name: 'description', content: 'Check PUBG Mobile user IDs with Cloudflare bypass' }
      ]
    }
  },
  runtimeConfig: {
    // Private keys (only available on server-side)
    // Public keys that are exposed to the client
    public: {
      apiBase: process.env.NODE_ENV === 'production' ? 'https://your-domain.com' : 'http://localhost:3000'
    }
  }
}) 
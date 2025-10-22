// main.js
import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import { createI18n } from 'vue-i18n'
import { createPinia } from 'pinia'

import App from './App.vue'

// Page Components
import Home from './pages/Home.vue'
import Settings from './pages/Settings.vue'

// ----------------------------
// Router Configuration
// ----------------------------
const routes = [
  { path: '/', component: Home },
  { path: '/settings', component: Settings },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

// ----------------------------
// i18n Configuration
// ----------------------------
const i18n = createI18n({
  legacy: false, // recommended for Vue 3
  locale: localStorage.getItem('lang') || 'en',
  fallbackLocale: 'en',
  messages: {}, // will be loaded dynamically
})

// ----------------------------
// Load Translations from Flask API
// ----------------------------
async function loadTranslations(locale) {
  try {
    const response = await fetch(`/api/translations/${locale}`)
    if (response.ok) {
      const messages = await response.json()

      console.log('Fetched translations:', messages)

      i18n.global.setLocaleMessage(locale, messages)
      i18n.global.locale.value = locale
      localStorage.setItem('lang', locale)
    } else {
      console.error(`Failed to fetch translations for ${locale}: ${response.status}`)
    }
  } catch (error) {
    console.error('Failed to load translations:', error)
  }
}

// ----------------------------
// Initialize App
// ----------------------------
async function initApp() {
  const app = createApp(App)
  const  pinia = createPinia()
  
  app.use(router)
  app.use(i18n)
  app.use(pinia)

  // Expose translation reloader globally (for Settings page, etc.)
  app.config.globalProperties.$loadTranslations = loadTranslations

  // Load the initial language before mounting
  const initialLocale = i18n.global.locale.value
  await loadTranslations(initialLocale)

  // Mount the app after translations are ready
  app.mount('#app')
}

initApp()

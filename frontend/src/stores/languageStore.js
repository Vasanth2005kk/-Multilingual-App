import { defineStore } from 'pinia'

export const useLanguageStore = defineStore('language', {
  state: () => ({
    availableLanguages: [],
    selectedLanguage: 'en'
  }),

  actions: {
    async fetchLanguages() {
        try {
          const response = await fetch('/api/languages')
          if (!response.ok) throw new Error('Failed to fetch languages')
          
          const data = await response.json()
          console.log("datas",data)
          this.availableLanguages = data   // expecting array like [{ code: 'en', name: 'English' }, ...]
        } catch (error) {
          console.error('Error fetching languages:', error)
          this.errorMessage = 'Unable to load languages. Please try again later.'
        }
      }
  }
})

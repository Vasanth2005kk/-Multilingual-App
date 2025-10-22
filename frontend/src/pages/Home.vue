<template>
  <div class="page home-page">
    <div class="content-wrapper">
      <!-- Left: Hero section -->
      <div class="hero">
        <h1>{{ $t('home.title') }}</h1>
        <p class="description">
          <br>{{ $t('home.description1') }}</br>
          <br>{{ $t('home.description2') }}</br>
          <br>{{ $t('home.description3') }}</br>
          <br>{{ $t('home.description4') }}</br>
        </p>
        <router-link to="/settings" class="cta-button">
          {{ $t('navbar.settings') }}
        </router-link>
      </div>

      <!-- Right: Language selector -->
      <div class="page-lang">
        <label class="language-label">{{ $t('settings.language_label') }}</label>
        <select v-model="selectedLanguage" @change="changeLanguage" class="language-select">
          <option value="en">{{ $t('settings.english') }}</option>
          <option value="ta">{{ $t('settings.tamil') }}</option>
          
        </select>
      </div>
    </div>
  </div>
</template>

<script>

export default {
  name: 'Home',
  data() {
    return {
      selectedLanguage: this.$i18n.locale,
      availableLanguages: [], // store languages received from eventBus
    }
  },
  methods: {
    changeLanguage() {
      this.$loadTranslations(this.selectedLanguage);
    }
  }
}
</script>


<style scoped>
/* Whole page background */
.home-page {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  min-height: 90vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 3rem 2rem;
  border-radius: 10px;
  margin: 10px;
}

/* Flex container for hero + language */
.content-wrapper {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  flex-wrap: wrap;
  max-width: 1200px;
  width: 100%;
  gap: 2rem;
}

/* Left: Hero text */
.hero {
  flex: 1 1 65%;
  max-width: 700px;
}

.hero h1 {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.description {
  font-size: 1rem;
  margin-bottom: 2rem;
  line-height: 2rem;
  text-align: justify;
}

/* Button */
.cta-button {
  display: inline-block;
  padding: 1rem 2rem;
  background: white;
  color: #667eea;
  text-decoration: none;
  border-radius: 5px;
  font-weight: bold;
  transition: transform 0.3s, box-shadow 0.3s;
}

.cta-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
}

/* Right: Language selection (white background removed) */
.page-lang {
  flex: 1 1 25%;
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 0.75rem;
  color: white;
}

/* Inline label + select */
.language-label {
  font-size: 1rem;
  font-weight: bold;
}

.language-select {
  padding: 0.6rem 1rem;
  border: 2px solid white;
  border-radius: 5px;
  font-size: 1rem;
  background: transparent;
  color: white;
  cursor: pointer;
  transition: all 0.3s;
}

.language-select option {
  color: #333;
}

.language-select:hover,
.language-select:focus {
  border-color: #fffbf2;
  outline: none;
}

/* Responsive layout */
@media (max-width: 900px) {
  .content-wrapper {
    flex-direction: column;
    align-items: center;
    text-align: center;
  }

  .page-lang {
    justify-content: center;
    margin-top: 2rem;
  }
}
</style>

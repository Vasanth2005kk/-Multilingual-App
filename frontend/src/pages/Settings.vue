<template>
  <div class="settings-page">
    <div class="container-fluid">
      <div class="row">
        <!-- Main Content -->
        <div class="col-12">
          <div class="main-card">
            <!-- Header with Progress Circle -->
            <div class="page-header">
              <div class="header-left">
                <h1>
                  <i class="bi bi-translate me-2"></i>
                  Translation Manager
                </h1>
              </div>
              
              <div class="header-right">
                <!-- Language Selector -->
                <div class="language-selector">
                  <label>Editing Language:</label>
                  <select 
                    v-model="selectedLanguage" 
                    class="form-select"
                  >
                    <option 
                      v-for="lang in availableLanguages.filter(l => l.code !== 'en')" 
                      :key="lang.code"
                      :value="lang.code"
                    >
                      {{ lang.name }}
                    </option>
                  </select>
                </div>

                <!-- Circular Progress -->
                <div class="progress-circle">
                  <svg width="80" height="80" viewBox="0 0 80 80">
                    <circle
                      cx="40"
                      cy="40"
                      r="32"
                      fill="none"
                      stroke="#e0e7ff"
                      stroke-width="8"
                    />
                    <circle
                      cx="40"
                      cy="40"
                      r="32"
                      fill="none"
                      :stroke="getProgressColor(getLanguageProgress(selectedLanguage))"
                      stroke-width="8"
                      stroke-linecap="round"
                      :stroke-dasharray="circumference"
                      :stroke-dashoffset="getProgressOffset(getLanguageProgress(selectedLanguage))"
                      transform="rotate(-90 40 40)"
                    />
                  </svg>
                  <div class="progress-text">
                    <div class="percentage">{{ getLanguageProgress(selectedLanguage) }}%</div>
                    <div class="lang-name">{{ getLanguageName(selectedLanguage) }}</div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Search and Filter Section -->
            <div class="search-section">
              <div class="search-bar">
                <i class="bi bi-search search-icon"></i>
                <input
                  v-model="searchQuery"
                  type="text"
                  class="form-control search-input"
                  placeholder="Search translations..."
                />
                <button 
                  v-if="searchQuery"
                  @click="searchQuery = ''"
                  class="btn-clear"
                >
                  <i class="bi bi-x-circle"></i>
                </button>
              </div>
            </div>

            <!-- Translations Table -->
            <div class="translations-section">
              <div class="section-header">
                <h5>
                  <i class="bi bi-table me-2"></i>
                  Translations Table
                </h5>
                <div class="stats-inline">
                  <span class="badge bg-primary">
                    {{ Object.keys(translations).length }} Total
                  </span>
                  <span class="badge bg-success">
                    {{ getCompletedCount() }} Completed in {{ getLanguageName(selectedLanguage) }}
                  </span>
                </div>
              </div>

              <div v-if="Object.keys(translations).length === 0" class="alert alert-info">
                <i class="bi bi-info-circle me-2"></i>
                No translations yet. Add your first translation above!
              </div>

              <div v-else class="table-responsive">
                <table class="table table-hover">
                  <thead>
                    <tr>
                      <th width="5%">#</th>
                      <th width="40%">
                        <i class="bi bi-flag-fill me-2"></i>
                        English (Default)
                      </th>
                      <th width="35%">
                        {{ getLanguageName(selectedLanguage) }} Translation
                      </th>
                      <th width="15%" class="text-center">Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="(key, index) in filteredKeys" :key="key">
                      <td class="align-middle text-center">
                        <span class="row-number">{{ index + 1 }}</span>
                      </td>
                      <td class="align-middle">
                        <div class="english-cell">
                          {{ translations[key]['en'] }}
                        </div>
                      </td>
                      <td class="align-middle">
                        <input
                          v-if="editingKey === key"
                          v-model="editValue"
                          type="text"
                          class="form-control"
                          :placeholder="`Enter ${getLanguageName(selectedLanguage)} translation...`"
                          @keyup.enter="saveEdit(key)"
                          @keyup.esc="cancelEdit"
                        />
                        <div v-else class="translation-display">
                          {{ translations[key][selectedLanguage] || '(empty)' }}
                        </div>
                      </td>
                      <td class="text-center align-middle">
                        <div class="action-buttons">
                          <template v-if="editingKey === key">
                            <button
                              @click="saveEdit(key)"
                              class="btn btn-success btn-sm"
                              title="Save (Enter)"
                            >
                              <i class="bi bi-check-lg"></i> Save
                            </button>
                            <button
                              @click="cancelEdit"
                              class="btn btn-secondary btn-sm"
                              title="Cancel (Esc)"
                            >
                              <i class="bi bi-x-lg"></i> Cancel
                            </button>
                          </template>
                          <template v-else>
                            <button
                              @click="startEdit(key)"
                              class="btn btn-warning btn-sm"
                              title="Edit"
                            >
                              <i class="bi bi-pencil"></i> Edit
                            </button>
                          </template>
                        </div>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>

export default {
  name: 'Settings',
  data() {
    return {
      selectedLanguage: 'ta',
      searchQuery: '',
      errorMessage: '',
      editingKey: null,
      editValue: '',
      nextId: 1,
      oldValue :'',
      newValue : '',
      circumference: 2 * Math.PI * 32, // Circle circumference for progress
      
      availableLanguages: [], // initially empty, will be loaded from API

      translations: {}
    };
  },
  mounted() {
    this.fetchLanguages()
    this.fetchTranslations()
  },
  computed: {
    sortedKeys() {
      return Object.keys(this.translations).sort((a, b) => parseInt(a) - parseInt(b));
    },
    filteredKeys() {
      if (!this.searchQuery.trim()) {
        return this.sortedKeys;
      }
      
      const query = this.searchQuery.toLowerCase();
      return this.sortedKeys.filter(key => {
        const englishText = this.translations[key]['en'].toLowerCase();
        const translationText = (this.translations[key][this.selectedLanguage] || '').toLowerCase();
        return englishText.includes(query) || translationText.includes(query);
      });
    },
  },
  methods: {
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
    },
    async fetchTranslations() {
      try {
        const res = await fetch('/api/datas')
        const data = await res.json()
        this.translations = data
        console.log(data.translations)  // view grouped translations
      } catch (err) {
        console.error('Error loading translations:', err)
      }
    },
    async updateTranslation(lang,oldValue,newValue) {
      try {
        const response = await fetch('/api/update_translation', {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({
            lang: lang,
            old_value: oldValue,
            new_value: newValue
          })
        });

        const result = await response.json();

        if (response.ok) {
          this.message = result.message;
        } else {
          this.message = result.error || result.message;
        }
      } catch (error) {
        this.message = "Error: " + error.message;
      }
    },
    selectLanguage(langCode) {
      this.selectedLanguage = langCode;
    },
    getLanguageName(code) {
      const lang = this.availableLanguages.find(l => l.code === code);
      return lang ? lang.name : code.toUpperCase();
    },
    getLanguageProgress(langCode) {
      if (langCode === 'en') return 100;
      
      const totalKeys = Object.keys(this.translations).length;
      if (totalKeys === 0) return 0;
      
      let completed = 0;
      Object.keys(this.translations).forEach(key => {
        if (this.translations[key][langCode] && this.translations[key][langCode].trim() !== '') {
          completed++;
        }
      });
      
      return Math.round((completed / totalKeys) * 100);
    },
    getProgressOffset(percentage) {
      return this.circumference - (percentage / 100) * this.circumference;
    },
    getProgressColor(percentage) {
      if (percentage === 100) return '#28a745';
      if (percentage >= 50) return '#ffc107';
      return '#dc3545';
    },
    getLanguageStatusIcon(langCode) {
      const progress = this.getLanguageProgress(langCode);
      if (progress === 100) return 'bi-check-circle-fill';
      if (progress > 0) return 'bi-hourglass-split';
      return 'bi-circle';
    },
    getLanguageStatusColor(langCode) {
      const progress = this.getLanguageProgress(langCode);
      if (progress === 100) return '#28a745';
      if (progress > 0) return '#ffc107';
      return '#6c757d';
    },
    startEdit(key) {
      this.editingKey = key;
      this.editValue = this.translations[key][this.selectedLanguage] || '';
      this.oldValue = this.editValue
    },
    async saveEdit(key) {
      this.translations[key][this.selectedLanguage] = this.editValue;
      this.newValue =  this.editValue
      
      if (this.newValue !== this.oldValue){
        // console.log("new word :",this.newValue)
        // console.log("old word :",this.oldValue)
        // console.log("key :",this.selectedLanguage)
        await this.updateTranslation(this.selectedLanguage,this.oldValue,this.newValue)
        window.location.reload(true)
        
      }
      this.editingKey = null;
      this.editValue = '';
    },
    cancelEdit() {
      this.editingKey = null;
      this.editValue = '';
    },
    getCompletedCount() {
      let count = 0;
      Object.keys(this.translations).forEach(key => {
        if (this.translations[key][this.selectedLanguage] && 
            this.translations[key][this.selectedLanguage].trim() !== '') {
          count++;
        }
      });
      return count;
    }
  }
};
</script>

<style scoped>
@import url('https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.1/font/bootstrap-icons.css');

* {
  box-sizing: border-box;
}

/* ===== TABLE LAYOUT FIX ===== */
.table {
  table-layout: fixed;
  width: 100%;
  border-collapse: collapse;
}

.table th,
.table td {
  vertical-align: middle !important;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  padding: 0.75rem;
}

.table th:nth-child(2),
.table td:nth-child(2) {
  width: 40%;
}

.table th:nth-child(3),
.table td:nth-child(3) {
  width: 35%;
}

.table td input.form-control {
  width: 100%;
  height: 38px;
  font-size: 0.95rem;
  padding: 6px 10px;
  border: 2px solid #667eea;
  border-radius: 6px;
  transition: all 0.2s ease;
  box-sizing: border-box;
}

.table td input.form-control:focus {
  outline: none;
  border-color: #764ba2;
  box-shadow: 0 0 0 3px rgba(118, 75, 162, 0.15);
}

.table tbody tr {
  height: 60px;
}

.translation-display {
  display: inline-block;
  width: 100%;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  color: #333;
}

/* ===== SETTINGS PAGE ===== */
.settings-page {
  /* background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); */
  padding: 20px;
}

.sidebar-icons,
.language-icons-vertical {
  display: none;
}

/* ===== MAIN CARD ===== */
.main-card {
  background: white;
  border-radius: 20px;
  padding: 35px;
}

/* ===== PAGE HEADER ===== */
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
  padding-bottom: 25px;
  border-bottom: 3px solid #e0e7ff;
}

.header-left h1 {
  color: #667eea;
  font-weight: 700;
  margin: 0;
  font-size: 2rem;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 25px;
}

/* ===== LANGUAGE SELECTOR ===== */
.language-selector {
  display: flex;
  align-items: center;
  gap: 10px;
}

.language-selector label {
  font-weight: 600;
  color: #4a5568;
  white-space: nowrap;
}

.form-select {
  border: 2px solid #e0e7ff;
  border-radius: 10px;
  padding: 10px 16px;
  font-weight: 600;
  color: #667eea;
  min-width: 180px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.form-select:focus {
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
  outline: none;
}

/* ===== PROGRESS CIRCLE ===== */
.progress-circle {
  position: relative;
  width: 80px;
  height: 80px;
}

.progress-circle svg {
  transform: scaleY(-1);
}

.progress-text {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  text-align: center;
}

.percentage {
  font-size: 1rem;
  font-weight: 700;
  color: #667eea;
  line-height: 1;
}

.lang-name {
  font-size: 0.90rem;
  color: #718096;
  font-weight: 600;
  margin-top: 2px;
}

/* ===== SEARCH SECTION ===== */
.search-section {
  background: linear-gradient(135deg, #f8f9ff 0%, #f0f0ff 100%);
  padding: 25px;
  border-radius: 15px;
  border: 2px solid #e0e7ff;
  margin-bottom: 30px;
}

.search-bar {
  position: relative;
  display: flex;
  align-items: center;
}

.search-icon {
  position: absolute;
  left: 18px;
  color: #667eea;
  font-size: 1.2rem;
  z-index: 1;
}

.search-input {
  padding-left: 50px !important;
  padding-right: 45px !important;
  border: 2px solid #e0e7ff;
  border-radius: 12px;
  padding: 14px 20px;
  font-size: 1rem;
  width: 100%;
  transition: all 0.3s ease;
}

.search-input:focus {
  border-color: #667eea;
  box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.1);
  outline: none;
}

.btn-clear {
  position: absolute;
  right: 12px;
  background: transparent;
  border: none;
  color: #718096;
  cursor: pointer;
  padding: 5px;
  display: flex;
  align-items: center;
  transition: all 0.3s ease;
}

.btn-clear:hover {
  color: #dc3545;
  transform: scale(1.1);
}

.btn-clear i {
  font-size: 1.2rem;
}

/* ===== FORM + BUTTONS ===== */
.form-control {
  border: 2px solid #e0e7ff;
  border-radius: 10px;
  padding: 12px 16px;
  flex: 1;
  transition: all 0.3s ease;
}

.form-control:focus {
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
  outline: none;
}

.btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 10px;
  padding: 12px 30px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  white-space: nowrap;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4);
}

/* ===== TRANSLATIONS SECTION ===== */
.translations-section {
  margin-top: 30px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.section-header h5 {
  color: #4a5568;
  font-weight: 600;
  margin: 0;
}

.stats-inline {
  display: flex;
  gap: 10px;
}

.badge {
  padding: 8px 16px;
  border-radius: 20px;
  font-weight: 600;
  font-size: 0.85rem;
}

/* ===== TABLE STYLES ===== */
.table-responsive {
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.table thead {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.table thead th {
  padding: 16px;
  font-weight: 600;
  border: none;
  font-size: 0.95rem;
}

.table tbody td {
  padding: 16px;
  vertical-align: middle;
}

.table tbody tr:hover {
  /* background-color: #f8f9ff; */
  background-color: #d6dbff;
  
}

.row-number {
  display: inline-block;
  width: 30px;
  height: 30px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 50%;
  line-height: 30px;
  font-weight: 700;
  font-size: 0.9rem;
  text-align: center;
}

.english-cell {
  color: #2d3748;
  font-weight: 600;
  font-size: 1rem;
  padding: 8px 12px;
  background: #f7fafc;
  border-radius: 8px;
  display: inline-block;
}

/* ===== ACTION BUTTONS ===== */
.action-buttons {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
}

.action-buttons .btn {
  border: none;
  padding: 8px 14px;
  border-radius: 8px;
  font-weight: 600;
  font-size: 0.9rem;
  display: flex;
  align-items: center;
  gap: 6px;
  transition: all 0.25s ease;
}

.btn-warning {
  background-color: #ffc107;
  color: #212529;
}
.btn-warning:hover {
  background-color: #ffca2c;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(255, 193, 7, 0.3);
}

.btn-success {
  background-color: #28a745;
  color: white;
}
.btn-success:hover {
  background-color: #218838;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(40, 167, 69, 0.3);
}

.btn-secondary {
  background-color: #6c757d;
  color: white;
}
.btn-secondary:hover {
  background-color: #5a6268;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(108, 117, 125, 0.3);
}


.action-buttons i {
  font-size: 1rem;
  margin-right: 2px;
}

/* ===== ALERTS ===== */
.alert {
  border-radius: 12px;
  border: none;
  padding: 16px 20px;
}

.alert-danger {
  background-color: #fee;
  color: #c53030;
}

.alert-info {
  background-color: #e6f7ff;
  color: #0c5460;
}

/* ===== RESPONSIVE ===== */
@media (max-width: 992px) {
  .page-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 20px;
  }
  .header-right {
    width: 100%;
    justify-content: space-between;
  }
}
</style>

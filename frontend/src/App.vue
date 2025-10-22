<template>
    <div class="app">
      <nav class="navbar">
        <div class="nav-container">
          <router-link to="/" class="logo">🌐 Multilingual App</router-link>
          <ul class="nav-links">
            <li><router-link to="/">{{ $t('navbar.home') }}</router-link></li>
            <li><router-link to="/settings">{{ $t('navbar.settings') }}</router-link></li>
          </ul>
        </div>
      </nav>
  
      <main class="main-content">
        <router-view />
      </main>
  
    </div>
</template>
  
<script>
export default {
  name: 'App',
}
</script>
  
<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  background: #f5f7fa;
  color: #333;
}

.app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.navbar {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 0;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  position: sticky;
  top: 0;
  z-index: 100;
}

.nav-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 1rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo {
  font-size: 1.5rem;
  font-weight: bold;
  text-decoration: none;
  color: white;
  transition: opacity 0.3s;
}

.logo:hover {
  opacity: 0.9;
}

.nav-links {
  display: flex;
  list-style: none;
  gap: 2rem;
}

.nav-links a {
  color: white;
  text-decoration: none;
  font-size: 1rem;
  transition: opacity 0.3s;
  padding: 0.5rem 0;
}

.nav-links a:hover {
  opacity: 0.8;
}

.nav-links router-link.router-link-active {
  border-bottom: 2px solid white;
}

@media (max-width: 768px) {
  .nav-container {
    flex-direction: column;
    gap: 1rem;
  }

  .nav-links {
    flex-direction: column;
    gap: 1rem;
  }

}
</style>
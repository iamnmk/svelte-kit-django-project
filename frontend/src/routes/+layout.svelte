<main class="page">
  <header class="header">
    <h1>Chill Notes</h1>
    <p class="subtle">SvelteKit + Django REST (no auth)</p>
  </header>
  <div class="content">
    <slot />
  </div>
</main>

<style>
  .page {
    max-width: 860px;
    margin: 24px auto;
    padding: 0 16px;
    font-family: system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial, sans-serif;
  }
  .header {
    margin-bottom: 18px;
  }
  .subtle {
    color: #666;
    margin-top: 4px;
  }
  .content {
    background: #fff;
    border: 1px solid #eee;
    border-radius: 10px;
    padding: 18px;
  }
</style>


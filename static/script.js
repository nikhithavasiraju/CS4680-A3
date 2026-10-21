const form = document.getElementById('study-form');
const button = document.getElementById('generate-btn');
const result = document.getElementById('result');
const emptyState = document.getElementById('empty-state');
const statusText = document.getElementById('status');
const modeBadge = document.getElementById('mode-badge');

function escapeHtml(value) {
  return value.replace(/[&<>'"]/g, char => ({'&':'&amp;','<':'&lt;','>':'&gt;',"'":'&#039;','"':'&quot;'}[char]));
}

function renderMarkdown(text) {
  const lines = text.split('\n');
  let html = '';
  let listOpen = false;
  for (const rawLine of lines) {
    const line = rawLine.trim();
    if (!line) { if (listOpen) { html += '</ul>'; listOpen = false; } continue; }
    if (line.startsWith('## ')) {
      if (listOpen) { html += '</ul>'; listOpen = false; }
      html += `<h2>${escapeHtml(line.slice(3))}</h2>`;
    } else if (/^[-*] /.test(line)) {
      if (!listOpen) { html += '<ul>'; listOpen = true; }
      html += `<li>${escapeHtml(line.slice(2))}</li>`;
    } else if (/^\d+\. /.test(line)) {
      if (!listOpen) { html += '<ul>'; listOpen = true; }
      html += `<li>${escapeHtml(line.replace(/^\d+\. /, ''))}</li>`;
    } else {
      if (listOpen) { html += '</ul>'; listOpen = false; }
      html += `<p>${escapeHtml(line)}</p>`;
    }
  }
  if (listOpen) html += '</ul>';
  return html;
}

form.addEventListener('submit', async (event) => {
  event.preventDefault();
  const payload = Object.fromEntries(new FormData(form).entries());
  button.disabled = true;
  button.querySelector('span').textContent = 'Creating your session...';
  statusText.textContent = 'StudyBuddy is thinking through your plan...';
  emptyState.classList.add('hidden');
  result.classList.remove('hidden');
  modeBadge.classList.add('hidden');
  result.innerHTML = '<p class="loading">Generating a personalized response...</p>';

  try {
    const response = await fetch('/api/generate', { method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify(payload) });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || 'Something went wrong.');
    result.innerHTML = renderMarkdown(data.answer);
    statusText.textContent = data.demo_mode ? 'Preview result generated without an API key.' : 'Generated with your AI tutor prompt.';
    if (data.demo_mode) modeBadge.classList.remove('hidden');
  } catch (error) {
    result.innerHTML = `<p><b>Could not generate the session.</b></p><p>${escapeHtml(error.message)}</p>`;
    statusText.textContent = 'Please check the form and try again.';
  } finally {
    button.disabled = false;
    button.querySelector('span').textContent = 'Generate study session';
  }
});

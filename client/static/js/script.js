document.getElementById('genBtn').addEventListener('click', async () => {
  const btn    = document.getElementById('genBtn');
  const output = document.getElementById('output');   // now a <div>
  const whimsy = document.getElementById('whimsy').value;

  btn.disabled = true;
  btn.textContent = 'Generating…';

  const controller = new AbortController();
  const timeoutId  = setTimeout(() => controller.abort(), 5000);

  try {
    const res = await fetch(`/generate?silliness=${encodeURIComponent(whimsy)}`, {
      method: 'GET',
      signal: controller.signal
    });
    clearTimeout(timeoutId);

    if (!res.ok) throw new Error(res.statusText);

    const { text } = await res.json();
    output.innerHTML = text;          // ⬅️ changed
  } catch (e) {
    if (e.name === 'AbortError') {
      output.innerHTML = "couldn't connect to server";  // ⬅️ changed
    } else {
      console.error(e);
      output.innerHTML = e.message || e;                // ⬅️ changed
    }
  } finally {
    btn.disabled = false;
    btn.textContent = 'Generate';
  }
});

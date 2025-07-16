document.getElementById('genBtn').addEventListener('click', async () => {
  const btn = document.getElementById('genBtn');
  const output = document.getElementById('output');
  const whimsy = document.getElementById('whimsy').value;      // get slider value

  btn.disabled = true;
  btn.textContent = 'Generating…';

  // AbortController for 5 s timeout
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), 5000);

  try {
    // include silliness query param
    const res = await fetch(`/generate?silliness=${encodeURIComponent(whimsy)}`, {
      method: 'GET',
      signal: controller.signal
    });
    clearTimeout(timeoutId);

    if (!res.ok) throw new Error(res.statusText);
    const { text } = await res.json();
    output.value = text;
  } catch (e) {
    if (e.name === 'AbortError') {
      output.value = "couldn't connect to server";
    } else {
      console.error(e);
      output.value = e.message || e;
    }
  } finally {
    btn.disabled = false;
    btn.textContent = 'Generate';
  }
});

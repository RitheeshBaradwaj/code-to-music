document.getElementById('uploadForm').addEventListener('submit', async (e) => {
  e.preventDefault();

  const form = e.target;
  const formData = new FormData(form);

  const res = await fetch('http://localhost:8000/analyze/', {
    method: 'POST',
    body: formData
  });

  const data = await res.json();

  if (res.ok) {
    // Show result
    document.getElementById('result').classList.remove('hidden');
    document.getElementById('metrics').textContent = JSON.stringify(data.metrics, null, 2);
    document.getElementById('mood').textContent = data.mood;

    // Set audio player
    const player = document.getElementById('player');
    player.src = `http://localhost:8000/${data.music_path}`;
    player.load();
  } else {
    alert("Something went wrong: " + (data.detail || "Check backend logs."));
  }
});

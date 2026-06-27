// web/script.js
async function loadPrayerTimes() {
    const res = await fetch("http://YOUR-FLY-URL.fly.dev:8080/api/namoz");
    const data = await res.json();
    document.getElementById('prayer-time').innerText = data.vaqtlar.bomdod;
}
loadPrayerTimes();
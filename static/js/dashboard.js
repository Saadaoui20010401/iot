async function loadLatest() {
    try {
        const res = await fetch("/latest/");
        const data = await res.json();

        document.getElementById("tempValue").textContent = data.temperature + " °C";
        document.getElementById("humValue").textContent = data.humidity + " %";

        const date = new Date(data.timestamp);
        const diffSec = Math.round((Date.now() - date) / 1000);

        // Conversion secondes en minutes et secondes restantes
        const minutes = Math.floor(diffSec / 60);
        const seconds = diffSec % 60;

        const timeAgo = `il y a : ${minutes} min ${seconds} sec (${date.toLocaleTimeString()})`;

        document.getElementById("tempTime").textContent = timeAgo;
        document.getElementById("humTime").textContent = timeAgo;

    } catch (e) {
        console.log("Erreur API :", e);
    }
}

loadLatest();         // chargement initial
setInterval(loadLatest, 5000); // mise à jour toutes les 5 secondes

// Simulasi user_id yang login
const userId = "user-uuid-from-session-or-token";

async function fetchRecommendations() {
    const response = await fetch(`/api/recommendations?user_id=${userId}`);
    const hotels = await response.json();

    const resultsContainer = document.getElementById("recommendations");
    resultsContainer.innerHTML = "";

    if (hotels.length === 0) {
        resultsContainer.innerHTML = "<p>Tidak ada rekomendasi yang sesuai.</p>";
        return;
    }

    hotels.forEach((hotel) => {
        const div = document.createElement("div");
        div.innerHTML = `
            <h3>${hotel.name}</h3>
            <p>Lokasi: ${hotel.location}</p>
            <p>Harga: Rp ${hotel.price}</p>
            <p>Fasilitas: ${hotel.facilities.join(", ")}</p>
        `;
        resultsContainer.appendChild(div);
    });
}

// Fetch recommendations when the page loads
fetchRecommendations();

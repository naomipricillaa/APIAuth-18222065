// search.js

document.getElementById("searchForm").addEventListener("submit", async (event) => {
    event.preventDefault();

    const location = document.getElementById("location").value;
    const minPrice = document.getElementById("minPrice").value;
    const maxPrice = document.getElementById("maxPrice").value;
    const petCategory = document.getElementById("petCategory").value;
    const petSize = document.getElementById("petSize").value;
    const bookingFrom = document.getElementById("bookingFrom").value;
    const bookingTo = document.getElementById("bookingTo").value;

    // Validasi input bookingFrom dan bookingTo
    if (!bookingFrom || !bookingTo) {
        alert("Both 'Booking From' and 'Booking To' dates are required.");
        return;
    }
    if (new Date(bookingFrom) >= new Date(bookingTo)) {
        alert("'Booking From' date must be earlier than 'Booking To' date.");
        return;
    }

    const params = new URLSearchParams({
        location,
        min_price: minPrice,
        max_price: maxPrice,
        pet_category: petCategory,
        pet_size: petSize,
        booking_from: bookingFrom,
        booking_to: bookingTo,
    });

    try {
        const response = await fetch(`/api/hotels?${params.toString()}`);
        if (!response.ok) {
            throw new Error(`Error: ${response.statusText}`);
        }

        const hotels = await response.json();
        const resultsContainer = document.getElementById("hotelResults");
        resultsContainer.innerHTML = ""; // Kosongkan container sebelum menambahkan hasil baru

        // Periksa apakah hotels adalah array
        if (Array.isArray(hotels) && hotels.length > 0) {
            hotels.forEach((hotel) => {
                const div = document.createElement("div");
                div.className = "hotel-card";
                div.innerHTML = `
                    <h3>${hotel.name}</h3>
                    <p>Location: ${hotel.location}</p>
                    <p>Price: Rp ${hotel.price}</p>
                    <p>Pet Category: ${hotel.pet_category}</p>
                    <p>Pet Size: ${hotel.pet_size}</p>
                    <p>Available from: ${hotel.available_from} to ${hotel.available_to}</p>
                    <p>Facilities: ${hotel.facilities && hotel.facilities.length > 0 ? hotel.facilities.join(", ") : "No facilities available"}</p>
                    <button class="btn-book" data-hotel-id="${hotel.id}">Book</button>
                `;
                resultsContainer.appendChild(div);
            });

            // Tambahkan event listener untuk tombol "Book"
            document.querySelectorAll(".btn-book").forEach((button) => {
                button.addEventListener("click", async (event) => {
                    const hotelId = event.target.dataset.hotelId;
                    const userId = "user-id-placeholder"; // Ganti dengan ID pengguna yang sedang login
                    const checkIn = bookingFrom;
                    const checkOut = bookingTo;

                    try {
                        const bookingResponse = await fetch("/api/book", {
                            method: "POST",
                            headers: { "Content-Type": "application/json" },
                            body: JSON.stringify({ user_id: userId, hotel_id: hotelId, check_in: checkIn, check_out: checkOut }),
                        });

                        if (!bookingResponse.ok) {
                            throw new Error(`Error: ${bookingResponse.statusText}`);
                        }

                        const bookingResult = await bookingResponse.json();
                        alert(`Booking successful: ${bookingResult.message}`);
                    } catch (error) {
                        console.error("Error booking hotel:", error);
                        alert("Failed to book hotel. Please try again.");
                    }
                });
            });
        } else {
            // Tampilkan pesan jika hotel tidak ditemukan
            resultsContainer.innerHTML = "<p>No hotels found matching the criteria.</p>";
        }
    } catch (error) {
        console.error("Error fetching hotels:", error);
        const resultsContainer = document.getElementById("hotelResults");
        resultsContainer.innerHTML = `<p>Error: ${error.message}</p>`;
    }
});
document.addEventListener('DOMContentLoaded', () => {
    const placeDetailsSection = document.getElementById('place-details');
    const addReviewSection = document.getElementById('add-review');

    if (!placeDetailsSection) return; // Exit if not on place details page

    // Helper to get cookie
    function getCookie(name) {
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            const [key, value] = cookie.trim().split('=');
            if (key === name) return decodeURIComponent(value);
        }
        return null;
    }

    // Extract place ID from URL query string
    function getPlaceIdFromURL() {
        const params = new URLSearchParams(window.location.search);
        return params.get('id');
    }

    const placeId = getPlaceIdFromURL();
    const token = getCookie('token');

    // Show/hide review form based on authentication
    if (!token) {
        if (addReviewSection) addReviewSection.style.display = 'none';
    } else {
        if (addReviewSection) addReviewSection.style.display = 'block';
    }

    // Fetch place details from API
    async function fetchPlaceDetails() {
        try {
            const response = await fetch(`/api/v1/places/${placeId}`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    ...(token && { 'Authorization': `Bearer ${token}` })
                }
            });

            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
            const place = await response.json();
            displayPlaceDetails(place);
        } catch (error) {
            console.error("Error fetching place details:", error);
            placeDetailsSection.innerHTML = "<p>Failed to load place details.</p>";
        }
    }

    // Display place details dynamically
    function displayPlaceDetails(place) {
        placeDetailsSection.innerHTML = '';

        const title = document.createElement('h2');
        title.textContent = place.name;
        placeDetailsSection.appendChild(title);

        const desc = document.createElement('p');
        desc.textContent = place.description;
        placeDetailsSection.appendChild(desc);

        const location = document.createElement('p');
        location.innerHTML = `<strong>Location:</strong> ${place.city}, ${place.state}`;
        placeDetailsSection.appendChild(location);

        const price = document.createElement('p');
        price.innerHTML = `<strong>Price:</strong> $${place.price}`;
        placeDetailsSection.appendChild(price);

        if (place.amenities && place.amenities.length > 0) {
            const amenities = document.createElement('ul');
            amenities.innerHTML = `<strong>Amenities:</strong>`;
            place.amenities.forEach(a => {
                const li = document.createElement('li');
                li.textContent = a.name;
                amenities.appendChild(li);
            });
            placeDetailsSection.appendChild(amenities);
        }

        if (place.reviews && place.reviews.length > 0) {
            const reviews = document.createElement('div');
            reviews.innerHTML = `<h3>Reviews</h3>`;
            place.reviews.forEach(r => {
                const reviewDiv = document.createElement('div');
                reviewDiv.className = 'review';
                reviewDiv.innerHTML = `<strong>${r.user_name}:</strong> ${r.text}`;
                reviews.appendChild(reviewDiv);
            });
            placeDetailsSection.appendChild(reviews);
        }
    }

    // Initialize
    fetchPlaceDetails();
});

document.addEventListener('DOMContentLoaded', () => {
    const placeDetailsSection = document.getElementById('place-details');
    const addReviewSection = document.getElementById('add-review');
    const reviewForm = document.getElementById('review-form');

    if (!placeDetailsSection) return;  // Exit if not on place page

    // Helper: get cookie by name
    function getCookie(name) {
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            const [key, value] = cookie.trim().split('=');
            if (key === name) return decodeURIComponent(value);
        }
        return null;
    }

    // Extract place ID from URL
    function getPlaceIdFromURL() {
        const params = new URLSearchParams(window.location.search);
        return params.get('place_id');  // assumes URL is ?place_id=<id>
    }

    const placeId = getPlaceIdFromURL();
    const token = getCookie('token');

    // Show/hide add review form based on authentication
    if (!token) {
        addReviewSection.style.display = 'none';
        document.getElementById('login-link').style.display = 'block';
    } else {
        addReviewSection.style.display = 'block';
        document.getElementById('login-link').style.display = 'none';
        fetchPlaceDetails(token, placeId);
    }

    // Fetch place details from API
    async function fetchPlaceDetails(token, placeId) {
        try {
            const response = await fetch(`/api/v1/places/${placeId}`, {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${token}`
                }
            });

            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
            const place = await response.json();
            displayPlaceDetails(place);

        } catch (error) {
            console.error("Error fetching place details:", error);
        }
    }

    // Render place details
    function displayPlaceDetails(place) {
        placeDetailsSection.innerHTML = `
            <h2>${place.name}</h2>
            <p>${place.description}</p>
            <p><strong>Location:</strong> ${place.city}, ${place.state}</p>
            <p><strong>Price:</strong> $${place.price}</p>
            <p><strong>Amenities:</strong> ${place.amenities.join(', ')}</p>
            <h3>Reviews:</h3>
            <ul id="reviews-list">
                ${place.reviews.map(r => `<li>${r.user}: ${r.text}</li>`).join('')}
            </ul>
        `;
    }

    // Handle review form submission
    if (reviewForm) {
        reviewForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            const reviewText = document.getElementById('review-text').value.trim();
            if (!reviewText) return;

            try {
                const response = await fetch(`/api/v1/places/${placeId}/reviews`, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "Authorization": `Bearer ${token}`
                    },
                    body: JSON.stringify({ text: reviewText })
                });

                if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
                const newReview = await response.json();

                // Add new review to the list
                const reviewsList = document.getElementById('reviews-list');
                const li = document.createElement('li');
                li.textContent = `${newReview.user}: ${newReview.text}`;
                reviewsList.appendChild(li);

                // Clear the form
                reviewForm.reset();

            } catch (error) {
                console.error("Error submitting review:", error);
            }
        });
    }
});

// -------------------- EXISTING LOGIN / LOGOUT / MAIN PAGE CODE ABOVE --------------------
// (keep everything you already have)

// -------------------- PLACE DETAILS (Task 3) --------------------
document.addEventListener('DOMContentLoaded', () => {
    const placeDetailsSection = document.getElementById('place-details');
    const addReviewSection = document.getElementById('add-review');
    const reviewForm = document.getElementById('review-form');

    if (!placeDetailsSection) return; // Only run on place page

    // -------------------- Helper: Get cookie --------------------
    function getCookie(name) {
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            const [key, value] = cookie.trim().split('=');
            if (key === name) return decodeURIComponent(value);
        }
        return null;
    }

    // -------------------- Get Place ID from URL --------------------
    function getPlaceIdFromURL() {
        const params = new URLSearchParams(window.location.search);
        return params.get('id'); // expects ?id=<place_id>
    }

    const placeId = getPlaceIdFromURL();
    const token = getCookie('token');

    // -------------------- Check authentication --------------------
    if (!token) {
        if (addReviewSection) addReviewSection.style.display = 'none';
    } else {
        if (addReviewSection) addReviewSection.style.display = 'block';
    }

    // -------------------- Fetch Place Details --------------------
    async function fetchPlaceDetails() {
        try {
            const response = await fetch(`/api/v1/places/${placeId}`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    ...(token ? { 'Authorization': `Bearer ${token}` } : {})
                }
            });

            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);

            const place = await response.json();
            displayPlaceDetails(place);

        } catch (error) {
            console.error("Error fetching place details:", error);
            placeDetailsSection.innerHTML = '<p>Error loading place details.</p>';
        }
    }

    // -------------------- Display Place Details --------------------
    function displayPlaceDetails(place) {
        placeDetailsSection.innerHTML = `
            <h2>${place.name}</h2>
            <p>${place.description}</p>
            <p><strong>Location:</strong> ${place.city}, ${place.state}</p>
            <p><strong>Price:</strong> $${place.price}</p>
            <p><strong>Amenities:</strong> ${place.amenities.map(a => a.name).join(', ')}</p>
            <div id="reviews-section">
                <h3>Reviews</h3>
                ${place.reviews.length === 0 ? '<p>No reviews yet</p>' : ''}
                <ul id="reviews-list">
                    ${place.reviews.map(r => `<li>${r.user_name}: ${r.text}</li>`).join('')}
                </ul>
            </div>
        `;
    }

    // -------------------- Submit a Review --------------------
    if (reviewForm) {
        reviewForm.addEventListener('submit', async (event) => {
            event.preventDefault();

            const reviewText = document.getElementById('review-text').value.trim();
            if (!reviewText) return;

            try {
                const response = await fetch(`/api/v1/places/${placeId}/reviews`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                    },
                    body: JSON.stringify({ text: reviewText })
                });

                if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);

                const newReview = await response.json();
                const reviewsList = document.getElementById('reviews-list');
                if (reviewsList) {
                    const li = document.createElement('li');
                    li.textContent = `${newReview.user_name}: ${newReview.text}`;
                    reviewsList.appendChild(li);
                }

                // Clear form
                document.getElementById('review-text').value = '';

            } catch (error) {
                console.error("Error submitting review:", error);
                alert('Failed to submit review.');
            }
        });
    }

    // -------------------- Initialize --------------------
    fetchPlaceDetails();
});
// ---------------- PLACE DETAILS & REVIEWS ----------------
document.addEventListener('DOMContentLoaded', () => {
    const placeDetailsContainer = document.getElementById('place-details');
    const reviewsList = document.getElementById('reviews-list');
    const addReviewSection = document.getElementById('add-review');
    const reviewForm = document.getElementById('review-form');

    // Get place ID from URL
    function getPlaceIdFromURL() {
        const urlParams = new URLSearchParams(window.location.search);
        return urlParams.get('id');
    }

    const placeId = getPlaceIdFromURL();
    const token = getCookie('token');

    // Show add review form only if user is authenticated
    if (!token) {
        addReviewSection.style.display = 'none';
    } else {
        addReviewSection.style.display = 'block';
        fetchPlaceDetails(placeId, token);
    }

    // Fetch place details from API
    async function fetchPlaceDetails(placeId, token=null) {
        try {
            const headers = { 'Content-Type': 'application/json' };
            if (token) headers['Authorization'] = `Bearer ${token}`;

            const response = await fetch(`/api/v1/places/${placeId}`, { headers });

            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
            const place = await response.json();
            displayPlaceDetails(place);
        } catch (error) {
            console.error("Error fetching place details:", error);
        }
    }

    // Display place details and reviews
    function displayPlaceDetails(place) {
        if (!placeDetailsContainer) return;

        placeDetailsContainer.innerHTML = `
            <p><strong>Description:</strong> ${place.description}</p>
            <p><strong>Location:</strong> ${place.city}, ${place.state}</p>
            <p><strong>Price:</strong> $${place.price}</p>
            <p><strong>Amenities:</strong> ${place.amenities.map(a => a.name).join(', ')}</p>
        `;

        // Display reviews
        if (reviewsList) {
            const reviewsHTML = place.reviews.map(r => `
                <div class="review">
                    <p><strong>${r.user_name}:</strong> ${r.text}</p>
                </div>
            `).join('');
            reviewsList.innerHTML = `<h2>Reviews</h2>${reviewsHTML}`;
        }
    }

    // Submit a new review
    if (reviewForm) {
        reviewForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            const reviewText = document.getElementById('review-text').value.trim();
            const errorBox = document.getElementById('review-error');

            if (!reviewText) {
                if (errorBox) errorBox.textContent = "Review cannot be empty";
                return;
            }

            try {
                const response = await fetch(`/api/v1/places/${placeId}/reviews`, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "Authorization": `Bearer ${token}`
                    },
                    body: JSON.stringify({ text: reviewText })
                });

                if (!response.ok) {
                    const err = await response.json();
                    if (errorBox) errorBox.textContent = err.message || "Error submitting review";
                    return;
                }

                const newReview = await response.json();
                // Add the new review to the list
                if (reviewsList) {
                    const div = document.createElement('div');
                    div.className = 'review';
                    div.innerHTML = `<p><strong>${newReview.user_name}:</strong> ${newReview.text}</p>`;
                    reviewsList.appendChild(div);
                }

                // Clear form
                reviewForm.reset();
                if (errorBox) errorBox.textContent = '';
            } catch (error) {
                if (errorBox) errorBox.textContent = "Network error — cannot submit review";
                console.error("Review submission error:", error);
            }
        });
    }

    // Helper to get cookie
    function getCookie(name) {
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            const [key, value] = cookie.trim().split('=');
            if (key === name) return decodeURIComponent(value);
        }
        return null;
    }

    // Fetch details initially if authenticated
    if (token) fetchPlaceDetails(placeId, token);
});


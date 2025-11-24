document.addEventListener('DOMContentLoaded', () => {
    const reviewForm = document.getElementById('addReviewForm');

    // Helper to get cookie
    function getCookie(name) {
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            const [key, value] = cookie.trim().split('=');
            if (key === name) return decodeURIComponent(value);
        }
        return null;
    }

    // Check authentication
    const token = getCookie('token');
    if (!token) {
        // Redirect unauthenticated users
        window.location.href = '/';
        return;
    }

    // Get place ID from URL query parameters
    function getPlaceIdFromURL() {
        const params = new URLSearchParams(window.location.search);
        return params.get('place_id');
    }

    const placeId = getPlaceIdFromURL();

    if (reviewForm) {
        reviewForm.addEventListener('submit', async (event) => {
            event.preventDefault();

            const reviewText = document.getElementById('review-text').value.trim();
            const rating = parseInt(document.getElementById('rating').value);

            if (!reviewText || !rating) return;

            try {
                const response = await fetch(`/api/v1/places/${placeId}/reviews`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                    },
                    body: JSON.stringify({ review: reviewText, rating: rating })
                });

                if (response.ok) {
                    alert('Review submitted successfully!');
                    reviewForm.reset();
                } else {
                    const err = await response.json();
                    alert(`Failed to submit review: ${err.message || response.status}`);
                }
            } catch (error) {
                console.error('Error submitting review:', error);
                alert('Network error — cannot submit review.');
            }
        });
    }
});


document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');

    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            const email = document.getElementById("email").value;
    		const password = document.getElementById("password").value;

			try {
                await loginUser(email, password);
            } catch (error) {
                alert('Une erreur est survenue : ' + error.message);
            }
        });
    } else {
		checkAuthentication();
	}

	async function loginUser(email, password) {
      const response = await fetch(`http://127.0.0.1:5000/api/v1/auth/login`, {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json'
          },
          body: JSON.stringify({ email, password })
      });

	  if (response.ok) {
      	const data = await response.json();
      	document.cookie = `token=${data.access_token}; path=/; max-age=3600; Secure; SameSite=Strict`;
      	window.location.href = 'index.html';
        return;
  		} else {
			try {
            	const errorData = await response.json();
            	alert('Échec de la connexion : ' + (errorData.message || response.statusText));
        	} catch (e) {
            	alert('Échec de la connexion : ' + response.statusText);
        	}
  		}
  	}

	function checkAuthentication() {
    const token = getCookie('token');
    const currentPage = window.location.pathname;

    if (!token) {
        window.location.href = 'index.html';
        return;
    }

    // Si on est sur index.html
    if (currentPage.includes('index.html') || currentPage.endsWith('/')) {
        const loginLink = document.getElementById('login-link');
        if (loginLink) loginLink.style.display = 'none';
        fetchPlaces(token);
    }

    // Si on est sur place.html
    if (currentPage.includes('place.html')) {
        const addReviewSection = document.getElementById('add-review');
        if (addReviewSection) addReviewSection.style.display = 'block';
        fetchPlaceDetails(token, placeId);
    }
    }


	function getCookie(name) {
    const cookies = document.cookie.split(";");
        for (let cookie of cookies) {
            cookie = cookie.trim();
        if (cookie.startsWith(name + "=")) {
            return cookie.substring(name.length + 1);
        }
        }
        return null;
    }
	

	async function fetchPlaces(token) {
		const response = await fetch(`http://127.0.0.1:5000/api/v1/places`, {
			method: 'GET',
			headers: {
				'Authorization': `Bearer ${token}`
			}
		});

		if (!response.ok) {
			throw new Error('Erreur lors du chargement des lieux');
		}

		const places = await response.json();
		displayPlaces(places);
  	}

	function displayPlaces(places) {
      const placesList = document.getElementById('places-list');
    	if (!placesList) {
			return;
		}

		placesList.innerHTML = '';

		places.forEach(place => {
			const placeDiv = document.createElement('div');
			placeDiv.classList.add('place');
			placesList.appendChild(placeDiv)
			placeDiv.dataset.price = place.price;
		});
  	}

	document.getElementById('price-filter').addEventListener('change', (event) => {
    const selectedPrice = parseFloat(event.target.value);
    const placeElements = document.querySelectorAll('.place');

    placeElements.forEach(place => {
        const placePrice = parseFloat(place.dataset.price);
            if (isNaN(selectedPrice) || placePrice <= selectedPrice) {
                place.style.display = 'block';
            } else {
                place.style.display = 'none';
            }
        });
    });


	async function fetchPlaceDetails(token, placeId) {
        const response = await fetch(`http://127.0.0.1:5000/api/v1/places/${placeId}`, {
			method: 'GET',
			headers: {
				'Authorization': `Bearer ${token}`
			}
		});

        if (!response.ok) {
			throw new Error('Erreur lors du chargement des détails');
		}

        const data = await response.json();
		displayPlaceDetails(data);
  	}

	function displayPlaceDetails(place) {
        const container = document.getElementById('placeDetails');
        container.innerHTML = '';

        if (!place) {
        container.textContent = 'Aucun détail disponible.';
        return;
        }

        const name = document.createElement('h2');
        name.textContent = place.name;

        const description = document.createElement('p');
        description.textContent = place.description;

        const price = document.createElement('p');
        price.textContent = `Prix: ${place.price} €`;

        const amenities = document.createElement('ul');
        if (place.amenities && place.amenities.length > 0) {
            place.amenities.forEach(item => {
                const li = document.createElement('li');
                li.textContent = item;
                amenities.appendChild(li);
            });
        } else {
            amenities.textContent = 'Aucun équipement disponible.';
        }

        const reviews = document.createElement('div');
        if (place.reviews && place.reviews.length > 0) {
            place.reviews.forEach(review => {
                const p = document.createElement('p');
                p.textContent = `"${review.comment}" — ${review.user}`;
                reviews.appendChild(p);
            });
        } else {
            reviews.textContent = 'Aucun avis pour le moment.';
        }

        container.appendChild(name);
        container.appendChild(description);
        container.appendChild(price);
        container.appendChild(document.createElement('hr'));
        container.appendChild(amenities);
        container.appendChild(document.createElement('hr'));
        container.appendChild(reviews);
  	}

	function getPlaceIdFromURL() {
        const urlParams = new URLSearchParams(window.location.search);
        const placeId = urlParams.get('place_id');
        return placeId;
    }

    const placeId = getPlaceIdFromURL();
    const token = getCookie('token');
    checkAuthentication();

    const reviewForm = document.getElementById('review-form');

    if (reviewForm) {
        reviewForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            const reviewText = document.getElementById('review-text').value;
            await submitReview(token, placeId, reviewText);
        });
    }

	async function submitReview(token, placeId, reviewText) {
    const response = await fetch(`http://127.0.0.1:5000/api/v1/places/${placeId}/reviews`, {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ comment: reviewText })
    });
        handleResponse(response);
    }


	function handleResponse(response) {
    if (response.ok) {
        alert('Review submitted successfully!');
        const reviewInput = document.getElementById('review-text');
        if (reviewInput) reviewInput.value = '';
    } else {
        alert('Failed to submit review');
      }
  	}
});

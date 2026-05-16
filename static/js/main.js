document.addEventListener('DOMContentLoaded', () => {
    
    // Navbar scroll effect
    window.addEventListener('scroll', () => {
        const navbar = document.querySelector('.navbar');
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });

    // Fetch initial data
    fetchTrending();
    fetchRecommended();
    fetchMood('Happy');
    fetchSimilar('The Matrix');

    // Carousel buttons
    setupCarousels();

    // Mood buttons
    const moodBtns = document.querySelectorAll('.mood-pill');
    moodBtns.forEach(btn => {
        btn.addEventListener('click', (e) => {
            // Remove active class from all
            moodBtns.forEach(b => b.classList.remove('active'));
            // Add active to clicked
            e.target.classList.add('active');
            // Fetch mood movies
            fetchMood(e.target.dataset.mood);
        });
    });

    // Search functionality
    const searchInput = document.getElementById('searchInput');
    const searchContainer = document.getElementById('search-results-container');
    const mainContent = document.getElementById('main-content');
    let searchTimeout;

    searchInput.addEventListener('input', (e) => {
        clearTimeout(searchTimeout);
        const query = e.target.value.trim();
        
        if (query.length > 2) {
            searchTimeout = setTimeout(() => {
                fetchSearch(query);
            }, 500);
        } else if (query.length === 0) {
            searchContainer.classList.add('hidden');
            mainContent.style.display = 'block';
        }
    });

    // Modal close
    document.querySelector('.close-modal').addEventListener('click', () => {
        document.getElementById('movie-modal').style.display = 'none';
    });

    window.addEventListener('click', (e) => {
        const modal = document.getElementById('movie-modal');
        if (e.target === modal) {
            modal.style.display = 'none';
        }
    });

    // Setup all static buttons
    setupStaticButtons();

    // Onboarding Logic
    setupOnboarding();
});

function showToast(message) {
    const container = document.getElementById('toast-container');
    const toast = document.createElement('div');
    toast.className = 'toast';
    toast.innerText = message;
    container.appendChild(toast);
    
    setTimeout(() => {
        toast.remove();
    }, 3500);
}

function setupStaticButtons() {
    // Nav links
    document.querySelectorAll('.nav-links a').forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            document.querySelectorAll('.nav-links a').forEach(l => l.classList.remove('active'));
            link.classList.add('active');
            
            if(link.innerText === 'My List') {
                showMyList();
            } else {
                // Restore main content if it was hidden
                document.getElementById('search-results-container').classList.add('hidden');
                document.getElementById('main-content').style.display = 'block';
                if(link.innerText !== 'Home') {
                    showToast('Browsing ' + link.innerText);
                }
            }
        });
    });

    // Icons
    document.querySelector('.fa-bell').addEventListener('click', () => showToast('No new notifications'));
    document.querySelector('.profile-img').addEventListener('click', () => showToast('Profile settings coming soon!'));

    // Hero buttons
    document.querySelector('.hero .btn-info').addEventListener('click', () => {
        fetch(`/api/search?query=Matrix`)
            .then(res => res.json())
            .then(data => {
                if(data.length > 0) openModal(data[0]);
            });
    });

    // Modal action buttons
    const modalButtons = document.querySelectorAll('.modal-actions .btn-circle');
    // Plus button (Add to list)
    modalButtons[0].addEventListener('click', () => {
        const title = document.getElementById('modal-title').innerText;
        let watchlist = JSON.parse(localStorage.getItem('watchlist') || '[]');
        if(!watchlist.includes(title)) {
            watchlist.push(title);
            localStorage.setItem('watchlist', JSON.stringify(watchlist));
            showToast('Added "' + title + '" to My List!');
        } else {
            showToast('"' + title + '" is already in your list.');
        }
    });
    // Thumbs up
    modalButtons[1].addEventListener('click', () => showToast('Thanks for your feedback!'));
    // Thumbs down
    modalButtons[2].addEventListener('click', () => showToast('We will tune your recommendations.'));
}

function showMyList() {
    const watchlist = JSON.parse(localStorage.getItem('watchlist') || '[]');
    const container = document.getElementById('search-results');
    container.innerHTML = '';
    
    if(watchlist.length === 0) {
        container.innerHTML = '<p>Your list is empty. Add some movies!</p>';
        document.getElementById('search-results-container').querySelector('h2').innerText = 'My List';
        document.getElementById('search-results-container').classList.remove('hidden');
        document.getElementById('main-content').style.display = 'none';
        return;
    }
    
    // Fetch details for each watched movie
    // Note: In a real app we'd have an endpoint to fetch by array of IDs. Here we fetch via search.
    let fetchPromises = watchlist.map(title => fetch(`/api/search?query=${encodeURIComponent(title)}`).then(r => r.json()));
    
    Promise.all(fetchPromises).then(results => {
        results.forEach(res => {
            if(res.length > 0) {
                // Find exact match
                createMovieCard(res[0], 'search-results');
            }
        });
        document.getElementById('search-results-container').querySelector('h2').innerText = 'My List';
        document.getElementById('search-results-container').classList.remove('hidden');
        document.getElementById('main-content').style.display = 'none';
    });
}

function setupOnboarding() {
    const savedGenres = localStorage.getItem('user_genres');
    if (!savedGenres) {
        // Show onboarding if no preferences are saved
        document.getElementById('onboarding-modal').style.display = 'block';
    }

    const genreBtns = document.querySelectorAll('.genre-btn');
    const finishBtn = document.getElementById('finish-onboarding-btn');
    let selectedGenres = [];

    genreBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            btn.classList.toggle('selected');
            const genre = btn.dataset.genre;
            if (selectedGenres.includes(genre)) {
                selectedGenres = selectedGenres.filter(g => g !== genre);
            } else {
                selectedGenres.push(genre);
            }
            
            finishBtn.disabled = selectedGenres.length === 0;
        });
    });

    finishBtn.addEventListener('click', () => {
        if (selectedGenres.length > 0) {
            localStorage.setItem('user_genres', JSON.stringify(selectedGenres));
            document.getElementById('onboarding-modal').style.display = 'none';
            fetchRecommended(); // Re-fetch with new preferences
        }
    });
}

function setupCarousels() {
    const containers = document.querySelectorAll('.carousel-container');
    containers.forEach(container => {
        const carousel = container.querySelector('.carousel');
        const prevBtn = container.querySelector('.prev-btn');
        const nextBtn = container.querySelector('.next-btn');

        if(prevBtn && nextBtn) {
            prevBtn.addEventListener('click', () => {
                carousel.scrollBy({ left: -300, behavior: 'smooth' });
            });

            nextBtn.addEventListener('click', () => {
                carousel.scrollBy({ left: 300, behavior: 'smooth' });
            });
        }
    });
}

function createMovieCard(movie, containerId, hasMatchScore = false) {
    const container = document.getElementById(containerId);
    if (!container) return;
    
    const card = document.createElement('div');
    card.className = 'movie-card';
    card.onclick = () => openModal(movie);

    let matchHtml = '';
    if (hasMatchScore && movie.confidence) {
        matchHtml = `<div class="movie-card-match">${movie.confidence}% Match</div>`;
    }

    card.innerHTML = `
        <img src="${movie.poster}" alt="${movie.title}" loading="lazy">
        <div class="movie-card-info">
            <div class="movie-card-title">${movie.title}</div>
            ${matchHtml}
        </div>
    `;
    container.appendChild(card);
}

function fetchTrending() {
    fetch('/api/trending')
        .then(res => res.json())
        .then(data => {
            const container = document.getElementById('trending-movies');
            container.innerHTML = '';
            data.forEach(movie => createMovieCard(movie, 'trending-movies'));
        });
}

function fetchRecommended() {
    const savedGenres = localStorage.getItem('user_genres');
    
    if (savedGenres) {
        // Fetch personalized recommendations
        fetch('/api/recommend/preferences', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ genres: JSON.parse(savedGenres) })
        })
        .then(res => res.json())
        .then(data => {
            const container = document.getElementById('recommended-movies');
            container.innerHTML = '';
            data.forEach(movie => createMovieCard(movie, 'recommended-movies', true));
        });
    } else {
        // Fallback to trending or simple user 1
        fetch('/api/recommend/user?user_id=1')
            .then(res => res.json())
            .then(data => {
                const container = document.getElementById('recommended-movies');
                container.innerHTML = '';
                data.forEach(movie => createMovieCard(movie, 'recommended-movies', true));
            });
    }
}

function fetchMood(mood) {
    fetch(`/api/mood?mood=${mood}`)
        .then(res => res.json())
        .then(data => {
            const container = document.getElementById('mood-movies');
            container.innerHTML = '';
            data.forEach(movie => createMovieCard(movie, 'mood-movies'));
        });
}

function fetchSimilar(title) {
    fetch(`/api/recommend/movie?title=${encodeURIComponent(title)}`)
        .then(res => res.json())
        .then(data => {
            const container = document.getElementById('similar-movies');
            container.innerHTML = '';
            data.forEach(movie => createMovieCard(movie, 'similar-movies', true));
        });
}

function fetchSearch(query) {
    fetch(`/api/search?query=${encodeURIComponent(query)}`)
        .then(res => res.json())
        .then(data => {
            const container = document.getElementById('search-results');
            container.innerHTML = '';
            
            if (data.length > 0) {
                data.forEach(movie => createMovieCard(movie, 'search-results'));
            } else {
                container.innerHTML = '<p>No movies found.</p>';
            }
            
            document.getElementById('search-results-container').querySelector('h2').innerText = 'Search Results';
            document.getElementById('search-results-container').classList.remove('hidden');
            document.getElementById('main-content').style.display = 'none';
        });
}

function openModal(movie) {
    document.getElementById('modal-img').src = movie.poster;
    document.getElementById('modal-title').innerText = movie.title;
    document.getElementById('modal-desc').innerText = movie.description;
    document.getElementById('modal-cast').innerText = movie.cast || 'N/A';
    document.getElementById('modal-genres').innerText = movie.genres || 'N/A';
    document.getElementById('modal-mood').innerText = movie.mood || 'N/A';
    
    const matchScore = movie.confidence ? `${movie.confidence}% Match` : '90% Match';
    document.getElementById('modal-match').innerText = matchScore;

    if(movie.imdb_url) {
        document.getElementById('modal-play-btn').href = movie.imdb_url;
    } else {
        document.getElementById('modal-play-btn').href = "#";
    }

    document.getElementById('movie-modal').style.display = 'block';
}

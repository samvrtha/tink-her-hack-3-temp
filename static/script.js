// Fetch and display colleges (works for both initial load and search)
function fetchColleges(searchTerm = ' ') {
    const url = searchTerm ? `/colleges?search=${encodeURIComponent(searchTerm)}` : '/colleges';
    
    fetch(url, { cache: 'no-cache' })  // Prevent caching
        .then(response => response.json())
        .then(data => {
            const collegesList = document.getElementById('colleges-list');
            collegesList.innerHTML = ''; // Clear existing content

            data.forEach(college => {
                const collegeCard = document.createElement('div');
                collegeCard.className = 'college-card';
                collegeCard.innerHTML = `
                    <h3>${college.name}</h3>
                    <p><strong>Location:</strong> ${college.location}</p>
                    <p><strong>Courses Offered:</strong> ${college.courses_offered}</p>
                    <p><strong>Fees:</strong> ₹${college.fees}</p>
                    <p><strong>Ranking:</strong> ${college.ranking}</p>
                    <p><strong>Facilities:</strong> ${college.facilities}</p>
                    <p><strong>Website:</strong> <a href="${college.website}" target="_blank">Visit Website</a></p>
                `;
                collegesList.appendChild(collegeCard);
            });
        })
        .catch(error => console.error('Error:', error));
}

// Handle form submission
// Handle form submission
document.getElementById('search-form').addEventListener('submit', function (event) {
    event.preventDefault(); // Prevent default form behavior
    const searchTerm = document.querySelector('input[name="user_data"]').value.trim();
    
    if (!searchTerm) {
        // Clear input and reload all colleges
        document.querySelector('input[name="user_data"]').value = '';
        fetchColleges(); // Fetch all colleges
        return;
    }

    // Fetch filtered colleges
    fetchColleges(searchTerm);
});

// Load all colleges on initial page load
document.addEventListener('DOMContentLoaded', () => fetchColleges());
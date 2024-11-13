document.addEventListener("DOMContentLoaded", function() {
    const searchInput = document.getElementById("search-input");
    const suggestionsList = document.getElementById("suggestions");

    searchInput.addEventListener("input", function() {
        const query = this.value;
        
        if (query.length > 1) {
            fetch(`/search/autocomplete?q=${query}`)
                .then(response => response.json())
                .then(data => {
                    suggestionsList.innerHTML = "";
                    data.suggestions.forEach(suggestion => {
                        const suggestionItem = document.createElement("div");
                        suggestionItem.textContent = suggestion;
                        suggestionItem.addEventListener("click", function() {
                            searchInput.value = suggestion;
                            suggestionsList.innerHTML = "";
                        });
                        suggestionsList.appendChild(suggestionItem);
                    });
                });
        } else {
            suggestionsList.innerHTML = "";
        }
    });

    document.addEventListener("click", function(event) {
        if (!suggestionsList.contains(event.target) && event.target !== searchInput) {
            suggestionsList.innerHTML = "";
        }
    });
});
// Ghi nhớ bộ lọc đã chọn sau khi tải lại trang
document.addEventListener('DOMContentLoaded', function() {
    const contentTypeRadios = document.querySelectorAll('input[name="content_type"]');
    const selectedContentType = new URLSearchParams(window.location.search).get('content_type') || 'all';

    contentTypeRadios.forEach(radio => {
        if (radio.value === selectedContentType) {
            radio.checked = true;
        }
    });
});

// static/script.js

document.addEventListener("DOMContentLoaded", function () {
    // Fade in the page on load
    document.body.classList.add('fade-in');

    // Fade out the page on navigation
    window.addEventListener('beforeunload', function () {
        document.body.classList.remove('fade-in');
    });
});


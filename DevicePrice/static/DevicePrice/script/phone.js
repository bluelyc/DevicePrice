function toggleFilter(element) {
    const content = element.nextElementSibling;
    if (content.style.display === "none" || !content.style.display) {
        content.style.display = "block";
    } else {
        content.style.display = "none";
    }
}
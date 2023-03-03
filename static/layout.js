// Toggle account dropdown
function menuDropdown() {
    document.getElementById("account-menu").classList.toggle("show");
}

// Hide dropdowns when clicking outside
document.addEventListener("click", function(event) {

    if (event.target.id !== "account-button") {
        document.getElementById("account-menu").classList.remove("show")
    }
});
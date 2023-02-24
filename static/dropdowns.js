
// Toggle workout dropdown
function workoutDropdown() {
    document.getElementById("workoutData").classList.toggle("show");
}

// Toggle account dropdown
function accountDropdown() {
    document.getElementById("accountData").classList.toggle("show");
}

// Hide dropdowns when clicking outside
document.addEventListener("click", function(event) {

    if (event.target.id !== "workoutButton") {
        document.getElementById("workoutData").classList.remove("show")
    }

    if (event.target.id !== "accountButton") {
        document.getElementById("accountData").classList.remove("show")
    }

});
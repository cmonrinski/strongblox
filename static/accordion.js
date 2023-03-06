window.addEventListener('load', (event) => {

    var accordion = document.getElementsByClassName("accordion");
    var i;

    for (i = 0; i < acc.length; i++) {
        accordion[i].addEventListener("click", function() {
            /* Toggle between adding and removing the "active" class, to highlight the button that controls the panel */
            this.classList.toggle("highlight");

            /* Toggle between hiding and showing the active panel */
            var panel = this.nextElementSibling;
            if (panel.style.display === "block") {
                panel.style.display = "none";
                } else {
                panel.style.display = "block";
                }
        });
    }
});


// Counter for rows
let rowCounter = 1;

// Routine Row as an object
const form = document.querySelector("form");

// getElementById returns an object
const routineRow = document.getElementById("routine-row");

// Routine Row as an array of ids
const rowIds = routineRow.querySelectorAll("*[id]");

rowIds.forEach(function(element){
    element.id = element.id + rowCounter;
});

// Run events after page loads
document.addEventListener("DOMContentLoaded", () => {
    
    // Add row to routine table
    document.querySelector("#add-row").onclick = function() {
        
        rowCounter++
        
        // Update table with new row
        let row = routineRow;
        let clone = row.cloneNode(true);
        
        // Update table row name
        // clone.id = clone.id.slice(0, -1);
        clone.id = clone.id + rowCounter;
        
        // Get all element ids in clone
        let cloneIds = clone.querySelectorAll("*[id]");

        // Add rowCounter to rowCounter column
        cloneIds[0].innerHTML = rowCounter;
        
        // Update slice off last digit of id name and then update each element id name
        cloneIds.forEach(function(element) {
            element.id = element.id.slice(0, -1);
            element.id = element.id + rowCounter;
            
        });

        // Update table body with new row and updated element ids
        form.appendChild(clone);

        // Clear values of text boxes
        document.getElementById(cloneIds[5].id).value = "";
        document.getElementById(cloneIds[6].id).value = "";
        document.getElementById(cloneIds[7].id).value = "";
        document.getElementById(cloneIds[8].id).value = "";

        // Clear placeholders if no historicaly match is found
        document.getElementById(cloneIds[5].id).placeholder = "Sets";
        document.getElementById(cloneIds[6].id).placeholder = "Reps";
        document.getElementById(cloneIds[7].id).placeholder = "Lbs";
        document.getElementById(cloneIds[8].id).placeholder = "Notes";
    }

    // Delete row from routine table
    document.querySelector("#delete-row").onclick = function() {
        if (rowCounter > 1) {
            var lastRow = document.getElementById("routine-row" + rowCounter);
            lastRow.remove();
            rowCounter--;
        }
    } 
    
    // Update variation dropdown when exercise dropdown changes
    form.addEventListener("change",function(event) {

        // Show drop down options for Variation if Exercise is changed
        if (event.target.id.startsWith("exercise")) {

            let targetExercise = event.target;
            let targetVariation = event.target.nextElementSibling;
    
            // Reset all menus on exercise change
            targetVariation.options.length = 1;
            targetVariation.selectedIndex = 0;

            // Get list of all variations based off selected exercise to load in dropdown
            for (let [key, value] of Object.entries(exerciseMap)) {
                if (key == targetExercise.value) {
                    let variationList = value;
    
                    // For each variation in variationList, include as option in select dropdown and add to dropdown
                    for (let [key, value] of variationList) {
                        
                        let v = document.getElementById(targetVariation.id);
                        let optVariation = document.createElement("option");
                        optVariation.value = value;
                        optVariation.text = value;
    
                        // This is the exerciseId however not currently necessary
                        let exerciseId = key;   

                        v.add(optVariation);
                    }
                }
            }
        }

        // If Equipment is selected, check historical data for most recent metrics
        if (event.target.getElementsByClassName("workout")) {

            let parent = event.target.parentNode.children;
            let exercise = parent[1];
            let variation = parent[2];
            let antirotation = parent[3];
            let equipment = parent[4];
            let sets = parent[5];
            let reps = parent[6];
            let weight = parent[7];
            let notes = parent[8];

            for (let i = 0; i < routineHistory.length; i++) {
                if (routineHistory[i][0] == exercise.value && routineHistory[i][1] == variation.value && routineHistory[i][2] == antirotation.value && routineHistory[i][3] == equipment.value) {
                                
                    // Assign last metrics of exercise and variation to placeholders
                    document.getElementById(sets.id).placeholder = routineHistory[i][4];
                    document.getElementById(reps.id).placeholder = routineHistory[i][5];
                    document.getElementById(weight.id).placeholder = routineHistory[i][6];
                    document.getElementById(notes.id).placeholder = routineHistory[i][7];
                    
                    // Break on first instance found
                    break;
                
                } else {
                    // Clear placeholders if no historicaly match is found
                    document.getElementById(sets.id).placeholder = "Sets";
                    document.getElementById(reps.id).placeholder = "Reps";
                    document.getElementById(weight.id).placeholder = "Lbs";
                    document.getElementById(notes.id).placeholder = "Notes";
                }
            }
        }
    });

    // Send json file of all routine data to flask app
    document.querySelector("form").addEventListener("submit", function (e) {

        // Prevent the normal submission of the form
        e.preventDefault();

        // Get HTML collection of routine data on submit
        let routineData = document.getElementsByClassName("routine");

        // This dictionary gets all exercises by element id
        let data = {};

        for (let i = 0; i < routineData.length; i++) {
            let key = routineData[i].id;
            let value = routineData[i].value;
            data[key] = value;
        }

        fetch("/routine", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify(data),
        });

        // Send user to success page (redirect doesn't load in Flask since POST is going through JSON)
        window.location.href = "http://192.168.1.38:5000/success";

    });
});
window.onload = function() {

    // Sound sources
    var whistle = new Audio("static/audio/whistle.wav");    // For start of any change to timer
    var click = new Audio("static/audio/click.wav");        // 3 second countdown
    var gong = new Audio("static/audio/gong.wav");          // For completion
    var tock = new Audio("static/audio/tock.wav");          // potential for metronome
    var blop = new Audio("static/audio/blop.wav");          // I like this best for metronome
    
    // Preset values for Tabata Timer
    var preActivityTime = 10;
    var activityTime = 20;
    var restTime = 10;
    var cyclesGoal = 8;
    var routinesGoal = 3;
    var recoveryTime = 120;
    var metronomeTime = 1;

    
    // Default settings
    var seconds = preActivityTime;
    var timerOn = false;
    var metronomeOn = false;
    var timerDetail = ""; // "pre", "active", "rest", "recovery", "complete", "pause", "resume", "reset"
    var interval;
    var cyclesCount = 0;
    var routinesCount = 0;

    // Input for values to update
    var preActivityInput = document.getElementById("pre-activity");
    var activityInput = document.getElementById("activity");
    var restInput = document.getElementById("rest");
    var cyclesInput = document.getElementById("cycles-goal");
    var routinesInput = document.getElementById("routines-goal");
    var recoveryInput = document.getElementById("recovery");
    var metronomeInput = document.getElementById("metronome");
    var updateButton = document.getElementById("update");

    // Start, Pause and End buttons
    var startButton = document.getElementById("start-button");
    var pauseButton = document.getElementById("pause-button");
    var endButton = document.getElementById("end-button");

    // Toggle options
    var changeWhistle = document.getElementById("change-whistle");
    var leadingClicks = document.getElementById("leading-clicks");
    var metronomeTocks = document.getElementById("metronome-tocks");
    var changeVibrate = document.getElementById("change-vibrate");

    console.log(changeWhistle);
    console.log(leadingClicks);
    console.log(metronomeTocks);
    console.log(changeVibrate);

    // Timer status and seconds counter
    var status = document.getElementById("status-view");
    var secondsView = document.getElementById("seconds-view");
    var cyclesView = document.getElementById("cycles-view");
    var routinesView = document.getElementById("routines-view");
    
    // Initial loading of the timer view
    secondsView.innerText = "-";
    cyclesView.innerText = "Cycles: " + cyclesCount + " / " + cyclesGoal;
    routinesView.innerText = "Routines: " + routinesCount + " / " + routinesGoal;
    pauseButton.disabled = true;

    // Update button to change timer's timings
    updateButton.onclick = function() {
        preActivityTime = Math.floor(preActivityInput.value * 1);
        activityTime = Math.floor(activityInput.value * 1);
        restTime = Math.floor(restInput.value * 1);
        cyclesGoal = Math.floor(cyclesInput.value * 1);
        routinesGoal = Math.floor(routinesInput.value * 1);
        recoveryTime = Math.floor(recoveryInput.value * 1);
        metronomeTime = Math.floor(metronomeInput.value * 1);
    }

    // Start timer at the beginning
    startButton.onclick = function() {
        timerOn = true;
        startButton.disabled = true;
        pauseButton.disabled = false;
        timerDetail = "pre";
        seconds = seconds - 1;
        interval = setInterval(countdownSeconds, 1000);
        changeToPre();
    }
    
    pauseButton.onclick = function() {
        // rememberTimer = timerDetail;
        // rememberSeconds = seconds;
        // rememberStatus = status.innerText;
        if (timerOn == true) {
            timerOn = false;
            startButton.disabled = true;
            pauseButton.innerText = "Resume";
            status.innerText = "Paused";
            timerDetail = "pause";
        } else {
            timerOn = true;
            startButton.disabled = true;
            pauseButton.innerText = "Pause";
            status.innerText = rememberStatus;
            timerDetail = rememberTimer;
            // seconds = rememberSeconds;
            // interval = setInterval(countdownSeconds, 1000);
        }
    }
    
    // End timer and clear counts
    endButton.onclick = function() {
        timerOn = false;
        startButton.disabled = false;
        timerDetail = "reset";
        clearInterval(interval);
        secondsView.innerText = "-";
        document.body.style.backgroundColor = "white";
        cyclesCount = 0;
        cyclesView.innerText = "Cycles: " + cyclesCount + " / " + cyclesGoal;
        routinesCount = 0;
        routinesView.innerText = "Routines: " + routinesCount + " / " + routinesGoal;
        status.innerText = "Hello";
    }
    
    function countdownSeconds() {
        if (timerOn == true) {
            checkForStateChange();
            seconds -= 1;
            secondsView.innerText = seconds;
        }
    }

    function checkForStateChange() {
        if (leadingClicks.checked && (seconds == 4 || seconds == 3 || seconds == 2)) {
            click.play();
        }
        if (seconds == 1) {
            if (timerDetail == "pre") {
                console.log("If statmenet 0");
                timerDetail = "active";
                rememberTimer = timerDetail;
                routinesCount += 1;
                routinesView.innerText = "Routines: " + routinesCount + " / " + routinesGoal;
                changeToActive();
            // cycles completed, routines completed - timer is done
            } else if (timerDetail == "active" && cyclesGoal == cyclesCount && routinesGoal == routinesCount) {
                console.log("If statement 1");
                timerDetail = "complete";
                endNaturally();
            // cycles completed but still have more routines to go    
            } else if (timerDetail == "active" && cyclesGoal == cyclesCount && routinesGoal > routinesCount) {
                console.log("If statement 2");
                timerDetail = "recover";
                rememberTimer = timerDetail;
                changeToRecover();
            // Still have more cycles to go, change to rest.  
            } else if (timerDetail == "active" && cyclesGoal > cyclesCount && routinesGoal >= routinesCount) {
                seconds = restTime + 1;
                console.log("If statement 3");
                timerDetail = "rest";
                rememberTimer = timerDetail;
                changeToRest();
            // rest and recover always go to active
            } else if (timerDetail == "rest" || timerDetail == "recover") {
                console.log("If statement 4");
                timerDetail = "active";
                rememberTimer = timerDetail;
                changeToActive();
            }
        }
    }
    
    function changeToPre() {
        if(changeWhistle.checked) {
            whistle.play();
        }
        status.innerText = "Get ready!";
        rememberStatus = status.innerText;
        seconds = preActivityTime + 1;
    }
    
    function changeToActive() {
        if(changeWhistle.checked) {
            whistle.play();
        }
        cyclesCount += 1;
        cyclesView.innerText = "Cycles: " + cyclesCount + " / " + cyclesGoal;
        status.innerText = "Go!";
        rememberStatus = status.innerText;
        document.body.style.backgroundColor = "green";
        seconds = activityTime + 1;
    }
    
    function changeToRest() {
        if(changeWhistle.checked) {
            whistle.play();
        }
        status.innerText = "Rest up!";
        rememberStatus = status.innerText;
        document.body.style.backgroundColor = "yellow";
        // seconds = restTime + 1;
    }
    
    function changeToRecover() {
        if(changeWhistle.checked) {
            whistle.play();
        }
        // Update routinesCount, reset cyclesCount
        routinesCount += 1;
        cyclesCount = 0;
        status.innerText = "Relax, recoupe, breathe.";
        rememberStatus = status.innerText;
        cyclesView.innerText = "Cycles: - / -";
        routinesView.innerText = "Routines: " + routinesCount + " / " + routinesGoal;
        document.body.style.backgroundColor = "red";
        seconds = recoveryTime + 1;
    }

    function endNaturally() {
        
        if(changeWhistle.checked) {
            gong.play();
        }
        clearInterval(interval);
        seconds = activityTime;
        secondsView.innerText = "-";
        status.innerText = "Great Success!";
        secondsView.innerText = "!!!";
        document.body.style.backgroundColor = "white";
        cyclesCount = 0;
        routinesCount = 0;
    }
}
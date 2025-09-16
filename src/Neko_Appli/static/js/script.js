    // Send a request to the Flask app to move forward
function forwardMovement() {
    fetch('/move/forward');
}

function backwardMovement() {
    fetch('/move/backward');
}

function leftSideways() {
    fetch('/move/left');
}

function rightSideways() {
    fetch('/move/right');
}

function nwMovement() {
    fetch('/move/nw');
}

function neMovement() {
    fetch('/move/ne');
}

function swMovement() {
    fetch('/move/sw');
}

function seMovement() {
    fetch('/move/se');
}

function rotatingLeft() {
    fetch('/rotate/left');
}

function rotatingRight() {
    fetch('/rotate/right');
}

function stopMovement() {
    fetch('/stop');
}

function captureImage() {
    fetch('/capture/image')
}

function toggleAutoMode() {
    var autoModeButton = document.getElementById('autoModeButton');
    var modeParagraph = document.querySelector('.mode');
    var allButtons = document.querySelectorAll('.disable')

    fetch('/auto-mode')

    // Toggle the 'active' class
    autoModeButton.classList.toggle('active');

    // Set the background color directly based on the presence of the 'active' class
    if (autoModeButton.classList.contains('active')) {
        autoModeButton.style.backgroundColor = 'red';
        modeParagraph.textContent = 'Auto';

        // Disable other buttons and change opacity
        allButtons.forEach(function(disable) {
            disable.disabled = true;
            disable.style.opacity = '0.9';
        });
    } else {
        autoModeButton.style.backgroundColor = '';
        modeParagraph.textContent = 'Manual';

        // revert buttons back
        allButtons.forEach(function(button) {
            button.disabled = false;
            button.style.opacity = '1';
        });
    }

}

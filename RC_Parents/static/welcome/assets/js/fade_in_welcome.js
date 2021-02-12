var opacity = -100; 
var intervalID = 0; 
window.onload = fadeIn; 
  
function fadeIn() { 
    setInterval(show, 9); 
} 
  
function show() { 
    var body = document.getElementById("main-content"); 
    opacity = Number(window.getComputedStyle(body) 
               .getPropertyValue("opacity")); 
    if (opacity < 1) { 
        opacity = opacity + 0.01; 
        body.style.opacity = opacity 
    } 
    else { 
        clearInterval(intervalID); 
    } 
} 
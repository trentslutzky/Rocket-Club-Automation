function preload(){
	document.getElementById("loading").style.display = "none";
	document.getElementById("start-subheading").style.display = "block";
}
window.onload = preload;

function load(){
    	document.getElementById("loading").style.display = "block";
    	document.getElementById("start-subheading").style.display = "none";
	document.getElementById("id-warning").style.visibility = "hidden";
}

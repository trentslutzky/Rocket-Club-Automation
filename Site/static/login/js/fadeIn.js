function fade_in(event){
    if (!event) {
        event = window.event;
    };

    var el = (event.target || event.srcElement);
    
    frame.src = el.dataset.dest;
    page_heading.innerHTML = el.dataset.heading;
    el.backgroundColor = "red";
}
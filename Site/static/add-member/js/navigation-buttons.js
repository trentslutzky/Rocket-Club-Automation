frame = document.getElementById("main-page-iframe")
page_heading = document.getElementById("page-heading")

function button_add_member(){
    frame.src = "add-member.html";
}

function button_add_rf(){
    frame.src = "add-rf.html";
}

function button_certs(){
    frame.src = "https://rocketclubtools.com/certs";
}

function button_view_info(){
    frame.src = "view-info.html";
}

function navigation_button(event){
    if (!event) {
        event = window.event; // Older versions of IE use 
                              // a global reference 
                              // and not an argument.
    };

    var el = (event.target || event.srcElement); // DOM uses 'target';
                                                 // older versions of 
                                                 // IE use 'srcElement'
    frame.src = el.dataset.dest;
    page_heading.innerHTML = el.dataset.heading;
    el.backgroundColor = "red";
}
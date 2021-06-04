conf_text = document.getElementById("add-member-confirmation")
function add_button_clicked(){
    conf_text.innerHTML = 'Adding Member...';   
}

class_confirm = document.getElementById("class-rf-confirmation")
class_loading_gif = document.getElementById("class-loading-gif")
class_update_button = document.getElementById("class-rf-submit-button")
function class_rf_update(){
    class_confirm.innerHTML = 'Loading...';
    class_loading_gif.style.visibility = 'visible';
    class_update_button.style.opacity = '50%';
    class_update_button.style.pointerEvents = 'none';
}

class_load_confirm = document.getElementById("load-class-confirmation")
function load_class(){
    class_load_confirm.innerHTML = 'Loading...';
}
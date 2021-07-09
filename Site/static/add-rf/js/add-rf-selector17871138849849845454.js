var cat_select = document.getElementById("category-select")
var sub_cat_select = document.getElementById("subcategory-select")
var sub_cat_section = document.getElementById("subcategory-section")
var amount_field = document.getElementById("rf-amount-form")

var subcategory_placeholder = document.getElementById("subcategory-placeholder")

 // option groups
var rcl_optgroup = document.getElementById("rcl_optgroup")
var communities_optgroup = document.getElementById("communities_optgroup")

function category_select(){
    cat_val = cat_select.value;
    console.log(cat_val);
    sub_cat_select.selectedIndex = 0;
    
    if (cat_val == "rcl") {
        sub_cat_section.style.visibility = "visible";
        communities_optgroup.style.display = "none";
        rcl_optgroup.style.display = "";
        subcategory_placeholder.innerHTML = "Select a Subcategory...";
    }
    
    else if (cat_val == "communities") {
        sub_cat_section.style.visibility = "visible";
        communities_optgroup.style.display = "";
        rcl_optgroup.style.display = "none";
        subcategory_placeholder.innerHTML = "Select a community...";
    }
    
    else {
        sub_cat_section.style.visibility = "hidden";
        communities_optgroup.style.display = "";
        rcl_optgroup.style.display = "";
        amount_field.value = null;
    }
}

function sub_category_select(){
    subcat_val = sub_cat_select.value;
    if (subcat_val == "kahoot_1") {
        amount_field.value = 500;
    }
    else if (subcat_val == "kahoot_2") {
        amount_field.value = 250;
    }
    else if (subcat_val == "kahoot_3") {
        amount_field.value = 150;
    }
    else if (subcat_val == "parents_2_first") {
        amount_field.value = 3000;
    }
    else if (subcat_val == "parents_2_second") {
        amount_field.value = 500;
    }
    else if (subcat_val == "parents_2_third") {
        amount_field.value = 250;
    }
    else if (subcat_val == "futurists") {
        amount_field.value = 150;
    }
    else if (subcat_val == "talent_show") {
        amount_field.value = 500;
    }
    else {
        amount_field.value = null;
    }
}
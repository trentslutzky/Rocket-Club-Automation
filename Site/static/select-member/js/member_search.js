function member_search(){
    var input, filter, table, tr, td, i, m_id,m_name,m_class;
    input = document.getElementById("member-search-input");
    filter = input.value.toUpperCase();
    table = document.getElementById("member-search-table");
    tr = document.getElementsByClassName("member-search-row");
    no_result = document.getElementById("member-search-no-results");
    
    no_result.style.display = "none";
    var num_results = 0;
    
    for (i = 0; i < tr.length; i++) {
        var td_id = (tr[i].getElementsByTagName("td")[0].textContent || tr[i].getElementsByTagName("td")[0].innerText);
        var td_name = (tr[i].getElementsByTagName("td")[1].textContent || tr[i].getElementsByTagName("td")[1].innerText);
        var td_class = (tr[i].getElementsByTagName("td")[2].textContent || tr[i].getElementsByTagName("td")[2].innerText);
        var txtValue = td_id + td_name + td_class;
        if (txtValue.toUpperCase().indexOf(filter) > -1) {
            tr[i].style.display = "";
            num_results++;
        } else {
            tr[i].style.display = "none";
        }
    }
    
    if (num_results == 0){
        no_result.style.display = "";
    }
}

window.addEventListener('load', (event) => {
    document.getElementById("member-search-no-results").style.display = "none";
});

function memberClicked(member_uuid,dest){
    url = '/'+dest+'?m_uuid='+member_uuid
    console.log(url)
    window.location.href = url;
}
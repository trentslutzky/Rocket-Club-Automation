import React, { useState, useEffect } from 'react';
import styled, { css } from 'styled-components';
import { useLocation, useHistory } from 'react-router-dom';

import { Loading } from './Loading.jsx';
import { CardText, CardHeading, DashboardCard, PageNav, PageNavButton, PageNavButtonSelected, Page } from './DashboardComponents.jsx';
import * as SVGIcons from '../images/SVGIcons.jsx';

function searchFilter(event){
    var filter = event.target.value.toUpperCase();
    var table = document.getElementById("member-search-table");
    var tr = table.getElementsByTagName("tr");
    for (var i = 0; i < tr.length; i++) {
        var td_id = tr[i].getElementsByTagName("td")[0];
        var td_name = tr[i].getElementsByTagName("td")[1];
        var td_class = tr[i].getElementsByTagName("td")[2];
        if (td_id) {
            var txtValue_id = td_id.textContent || td_id.innerText;
            var txtValue_name = td_name.textContent || td_name.innerText;
            var txtValue_class = td_class.textContent || td_class.innerText;
            var txtValue = txtValue_id+txtValue_name+txtValue_class;
            if (txtValue.toUpperCase().indexOf(filter) > -1) {
                tr[i].style.display = "";
            } else {
                tr[i].style.display = "none";
            }
        }       
    }
}

function SelectMember(props) { 

    const [members,setMembers] = useState(null);
    const [dest, setDest] = useState(props.dest);

    const history = useHistory();
    const handleClick = (uuid) => history.push('/'+dest+'/'+uuid);

    function loadDestination(member_uuid){
        var url = '/'+dest+'/'+member_uuid
        props.history.push(url);
    }

    useEffect(() => {
        if(members == null){
            var API_KEY = 'gaiGGD3hpm6cddc67rgf';
            fetch('http://localhost:5000/api/members/?api_key='+API_KEY)
                .then(res => res.json())
                .then((result) => {
                    setMembers(result);
                });
        }
        setDest(props.dest);
    });

    function capitalizeFirstLetter(string) {
        return string.charAt(0).toUpperCase() + string.slice(1);
    }

    var page_title = dest.replace('-',' ').replace('member','Member').replace('rf','RF').trim();
    page_title = capitalizeFirstLetter(page_title);

    if(!members){
        return(
            <Page>
                <PageTitle>{page_title}</PageTitle>
                <Loading/>
            </Page>
        );
    }
    var members_list = members.result.map((m) => {     
        return(     
            <SelectableRow onClick={() => handleClick(m.member_uuid)} key={m.member_id}>
                <td>{m.member_id}</td>    
                <td>{m.name}</td>    
                <td>{m.team}</td>    
            </SelectableRow>    
        )           
    });
    return(
    <Page>
        <PageTitle>{page_title}</PageTitle>
        <DashboardCard>
                <MemberSearchLine>
                    <SearchIco xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" className="feather feather-search"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></SearchIco>
                    <SearchInput id="member-search" type="text" placeholder="Search for members..." onChange={searchFilter.bind(this)}/>
                </MemberSearchLine>
                <MemberSearchTableContainer>
                    <table id="member-search-table">
                        <thead>
                            <tr>   
                                <th>Member ID</th>
                                <th>Name</th>
                                <th>Class</th> 
                            </tr>
                        </thead>
                        <tbody>
                            { members_list }
                        </tbody>
                    </table>
                </MemberSearchTableContainer>
            </DashboardCard>
    </Page>
    );
}

const PageTitle = styled.h1`
    margin-bottom:-10px;
`;

const SearchIco = styled.svg`
    margin-top: 8px;
    margin-left: 8px;
    color: var(--accent-0);
    stroke-width: 3;
    stroke-linecap: round;
`;

const MemberSearchLine = styled.div`
    border: 2px solid var(--table-border);
    background: var(--table-row-select);
    border-radius: 5px;
    margin-top: 8px;
    display:flex;
    margin-bottom:15px;
`;

const SearchInput = styled.input`
    font-size: 1.05rem;
    padding-left: 35px;
    border: none;
    background: transparent;
    width: 100%;
    border-radius: 5px;
    margin-left: -28px;
    margin-bottom:0px;
`;

const MemberSearchTableContainer = styled.div`
    height:800px;
    overflow-y:scroll;
    border: 2px solid var(--table-border);
    border-radius: 5px;
    margin-top:10px;
    margin-bottom:10px;
`;

const SelectableRow = styled.tr`
    &:hover{
        background-color:var(--table-row-select);
    }
    cursor:pointer;
`;

export { SelectMember };


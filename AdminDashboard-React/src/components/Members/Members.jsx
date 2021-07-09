import React, { useState, useEffect } from 'react';
import styled, { css } from 'styled-components';
import { useParams } from 'react-router-dom';

import { Loading } from '../Loading.jsx';
import { CardText, CardHeading, DashboardCard, Page, PageNav, PageNavButton, PageNavButtonSelected } from '../DashboardComponents.jsx';

import { Detail } from './Detail.jsx';
import { Edit } from './Edit.jsx';
import { Certs } from './Certs.jsx';

import { API_KEY,URL } from '../api.js';

function Members(props) { 

    let { uuid } = useParams();

    const [page_state,setPage] = useState(0);
    const [member_detail,setMemberDetail] = useState(null)
    const [member_uuid, setMemberUUID] = useState(uuid);
    const [transactions,setTransactions] = useState(null);

    const [team_names, setTeamNames] = useState(['']);    
    const [team_options, setTeamOptions] = useState(    
        <option value="ashoietnaoisehntioaesnhtoien" label="Loading teams..." defaultValue/>    
    ); 

    var updating_details = false;
    var updating_transactions = false;
    var updating_teams = false;
    var forced_update = false;

    function resetInfo(data=null){
        updating_details = false;
        forced_update = true;
        if(data != null){
            document.getElementById("page_title_name").innerText = data.name;
            setMemberDetail(data);
        } else {
            updateMemberData();
        }
    }

    function updateMemberData(){
        console.log('getting member data...');
        fetch(URL+'/api/members/'+member_uuid+'?api_key='+API_KEY)    
            .then(res => res.json())    
            .then((member_data) => {    
                setMemberDetail(member_data.result[0])
                console.log('Got member data.');
            })
    }

    useEffect(() => {    
        if((member_detail == null && updating_details == false) 
            || (updating_details == false && forced_update == true)){
            updating_details = true;
            forced_update = false;
            updateMemberData();
        }    

        if(member_detail && transactions == null && updating_transactions == false){
            updating_transactions = true;
            console.log('loading transactions...');                                                                           
            fetch(URL+'/api/rf_transactions/?member_uuid='+member_uuid+'&api_key='+API_KEY)    
            .then(res => res.json())                              
                .then((member_transactions) => {                  
                    setTransactions(member_transactions);    
                    console.log('Got transactions.');
                });                                                                 
        }

        if(team_names.length == 1 && updating_teams == false){
            updating_teams = true;
            console.log('Getting team names');    
            fetch(URL+'/api/teams/teamnames?api_key='+API_KEY)    
                .then(res => res.json()).then((result) => {    
                    console.log(result.team_names);
                    setTeamNames(result.team_names);
                    setTeamOptions(
                        result.team_names.map((team_name)=>(
                            <option key={team_name} value={team_name} label={team_name}/>
                        ))
                    );
                    console.log('Got team names');
                });
        }
    });

    function handleNavButtonClicked(page){
        setPage(page);
    }

    function DynamicPageTitle() {
        return(
            <TitleContainer>
                <PageTitle>Members</PageTitle>
                {member_detail != null 
                    ? (<PageTitleName id="page_title_name">{member_detail.name}</PageTitleName>) 
                    : (<PageTitleName>Loading...</PageTitleName>)
                }
            </TitleContainer>
        );
    }

    function DynamicPage(){
        if(member_detail != null && transactions != null){
            if(page_state == 0){
                return (
                    <>
                    <PageNav>
                        <PageNavButtonSelected>Member Details</PageNavButtonSelected>
                        <PageNavButton onClick={() => handleNavButtonClicked(1)}>Edit Details</PageNavButton>
                        <PageNavButton onClick={() => handleNavButtonClicked(2)}>Awards & Certifications</PageNavButton>
                    </PageNav>
                        <Detail data={[member_detail,transactions]}/>
                    </>
                );
            }
            if(page_state ==  1){
                return (
                    <>
                    <PageNav>
                        <PageNavButton onClick={() => handleNavButtonClicked(0)}>Member Details</PageNavButton>
                        <PageNavButtonSelected>Edit Details</PageNavButtonSelected>
                        <PageNavButton onClick={() => handleNavButtonClicked(2)}>Awards & Certifications</PageNavButton>
                    </PageNav>
                    <Edit data={[member_detail,team_options]} refresh={resetInfo}/>
                    </>
                );
            }
            if(page_state == 2){
                return (
                    <>
                    <PageNav>
                        <PageNavButton onClick={() => handleNavButtonClicked(0)}>Member Details</PageNavButton>
                        <PageNavButton onClick={() => handleNavButtonClicked(1)}>Edit Details</PageNavButton>
                        <PageNavButtonSelected>Awards & Certifications</PageNavButtonSelected>
                    </PageNav>
                    <Certs data={member_detail} refresh={resetInfo}/>
                    </>
                );
            }
        } else {
            return (<Page><Loading /></Page>);
        }
    }

    return(
        <Page>
            <DynamicPageTitle />
            <DynamicPage />
        </Page>
    );

}

const PageTitle = styled.h1`
    margin-bottom:0px;
`;

const PageTitleName = styled.p`
    font-size:14px;
    margin-bottom:0px;
    margin-left:10px;
    color:var(--accent-0);
    font-weight:bold;
`;

const TitleContainer = styled.div`
    display:flex;
    align-items:baseline;
    margin:0px;
`;

const RemoveButton = styled.div`
    width: 20px;
    text-align: center;
    height: 20px;
    border-radius: 4px;
    color: red;
    &:hover{
        background-color:red;
        color:white;
    }
    cursor:pointer;
`;

const TableHeading = styled(CardHeading)`
    border-bottom: 1px solid var(--main-bg);
    height: 37px;
    margin-bottom: 0px;
    font-size: 20px;
    margin-top: 7px;
`;

const UUIDCardText = styled(CardText)`
    font-size:13px;
    margin:0px;
    color:grey;
    margin-bottom:2px;
`;

const BigUserIcon = styled.svg`
    width: 200px;
    background-color: var(--main-bg);
    border-radius: 5px;
    box-shadow: rgba(0, 0, 0, 0.37) 0px 0px 15px -8px;
    color: var(--accent-0);
    margin: 15px 30px 15px 0px;
`;

const RFTransactionsTable = styled.div`
    margin-top:30px;
    width:max-content;
    margin-bottom:100px;
`;

const TDMono = styled.td`
    font-family:monospace;
    font-size:12x;
`;

const StyledTable = styled.table`
    border: 3px solid var(--button-hover);
    border-radius: 11px;
    padding: 6px;
`;

export { Members };


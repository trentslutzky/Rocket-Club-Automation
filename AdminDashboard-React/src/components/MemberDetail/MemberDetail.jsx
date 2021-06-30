import React from 'react';
import styled, { css } from 'styled-components';
import { useLocation, useHistory } from 'react-router-dom';

import { Loading } from '../Loading.jsx';
import { CardText, CardHeading, DashboardCard, PageNav, PageNavButton, PageNavButtonSelected } from '../DashboardComponents.jsx';

import { Detail } from './Detail.jsx';
import { Edit } from './Edit.jsx';
import { Certs } from './Certs.jsx';

class MemberDetail extends React.Component { 
    constructor(props) {
        super(props);
        this.state = {
            page_state:0
        }
    }

    setPage(page_state_set) {
        this.setState({page_state:page_state_set});
    }

    render() {
        const { page_state } = this.state;
        if(page_state == 0) {
            return (
                <Page>
                    <PageNav>
                        <PageNavButtonSelected>Member Details</PageNavButtonSelected>
                        <PageNavButton onClick={() => this.setPage(1)}>Edit Details</PageNavButton>
                        <PageNavButton onClick={() => this.setPage(2)}>Awards & Certifications</PageNavButton>
                    </PageNav>
                    <Detail/>
                </Page>
                );
        }
        else if (page_state == 1){
            return(
                <Page>
                    <PageNav>
                        <PageNavButton onClick={() => this.setPage(0)}>Member Details</PageNavButton>
                        <PageNavButtonSelected>Edit Details</PageNavButtonSelected>
                        <PageNavButton onClick={() => this.setPage(2)}>Awards & Certifications</PageNavButton>
                    </PageNav>
                    <Edit/>
                </Page>
            );
        }
        else if (page_state == 2){
            return(
                <Page>
                    <PageNav>
                        <PageNavButton onClick={() => this.setPage(0)}>Member Details</PageNavButton>
                        <PageNavButton onClick={() => this.setPage(1)}>Edit Details</PageNavButton>
                        <PageNavButtonSelected>Awards & Certifications</PageNavButtonSelected>
                    </PageNav>
                    <Certs/>
                </Page>
            )
        }
    }
}

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

const Page = styled.div`
    margin-bottom:300px;
`;

const StyledTable = styled.table`
    border: 3px solid var(--button-hover);
    border-radius: 11px;
    padding: 6px;
`;

export { MemberDetail };


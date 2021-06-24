import React from 'react';
import styled, { css } from 'styled-components';
import { useLocation, useHistory } from 'react-router-dom';

import { Loading } from './Loading.jsx';

class EditMember extends React.Component { 
    constructor(props) {
        super(props);
        this.state = {
            member_uuid:null,
            member_detail:null,
            transactions:null
        }
    }

    componentDidMount () {
        var API_KEY = 'gaiGGD3hpm6cddc67rgf';
        let MEMBER_UUID = '619e2d83-b9b6-43fe-bbd2-f148f1d98f76';
        fetch('http://localhost:5000/api/rf_transactions/?member_uuid='+MEMBER_UUID+'&api_key='+API_KEY)
            .then(res => res.json())
            .then((result) => {
                fetch('http://localhost:5000/api/members/'+MEMBER_UUID+'?api_key='+API_KEY)
                    .then(res => res.json())
                    .then((member_data) => {
                        this.setState({
                            member_uuid:MEMBER_UUID,
                            member_detail:member_data.result[0],
                            transactions:result
                        });
                        console.log(member_data.result[0].name);
                        console.log(transactions);
                    });
            });
    }


    render() {
        const { member_uuid, member_detail, transactions } = this.state;
        if(member_uuid) {
            var transaction_list = transactions.result.map((transaction) => { 
                return(
                    <tr>
                        <td>{transaction.amount}</td>
                        <td>{transaction.type}</td>
                        <td>{transaction.subtype}</td>
                        <TDMono>{transaction.completed}</TDMono>
                    </tr>
                )
            });
            return (
                <Page>
                    <MemberCard>
                        <div>
                            <BigUserIcon xmlns="http://www.w3.org/2000/svg" class="ionicon" viewBox="0 0 512 512">
                                <title>Person Circle</title>
                                    <path fill="currentColor" d="M258.9 48C141.92 46.42 46.42 141.92 48 258.9c1.56 112.19 92.91 203.54 205.1 205.1 117 1.6 212.48-93.9 210.88-210.88C462.44 140.91 371.09 49.56 258.9 48zm126.42 327.25a4 4 0 01-6.14-.32 124.27 124.27 0 00-32.35-29.59C321.37 329 289.11 320 256 320s-65.37 9-90.83 25.34a124.24 124.24 0 00-32.35 29.58 4 4 0 01-6.14.32A175.32 175.32 0 0180 259c-1.63-97.31 78.22-178.76 175.57-179S432 158.81 432 256a175.32 175.32 0 01-46.68 119.25z"/>
                                <path fill="currentColor" d="M256 144c-19.72 0-37.55 7.39-50.22 20.82s-19 32-17.57 51.93C191.11 256 221.52 288 256 288s64.83-32 67.79-71.24c1.48-19.74-4.8-38.14-17.68-51.82C293.39 151.44 275.59 144 256 144z"/>
                            </BigUserIcon>
                        </div>
                        <div>
                            <CardHeading>{member_detail.name}</CardHeading>
                            <UUIDCardText>{member_detail.member_uuid}</UUIDCardText>
                            <CardText><b>Member ID:</b> {member_detail.member_id}</CardText>
                            <CardText><b>Team:</b> {member_detail.team}</CardText>
                            <CardText><b>Grad Date:</b> {member_detail.grad_date}</CardText>
                            <CardText><b>Rocket Fuel:</b></CardText>
                            <CardText><b>RCL Attendance Credits:</b></CardText>
                            <CardText><b>HQ Points:</b></CardText>
                        </div>
                    </MemberCard>
                    <RFTransactionsTable>
                        <table>
                            <thead>
                                <tr>
                                    <th>Amount</th>
                                    <th>Type</th>
                                    <th>Subtype</th>
                                    <th>Timestamp</th>
                                </tr>
                            </thead>
                            <tbody>
                                { transaction_list }
                            </tbody>
                        </table>
                    </RFTransactionsTable>
                </Page>
                );
        }
        else{
            return(
                <Loading />
            );
        }
    }
}


const CardText = styled.div`
    margin-bottom:8px;
`;

const CardHeading = styled(CardText)`
    margin:0px;
    font-size:1.8rem;
    font-weight:bold;
`;

const UUIDCardText = styled(CardText)`
    font-size:10px;
    color:grey;
`;

const MemberCard = styled.div`
    width: 650px;
    background-color: var(--button-foreground);
    padding: 19px;
    padding-bottom: 1px;
    padding-top: 1px;
    margin-top: 25px;
    border-radius: 5px;
    box-shadow: rgb(0, 0, 0) 0px 0px 12px -8px;
    display:flex;
    align-items:center;
    border-top:5px solid black;
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
`;

const Page = styled.div`
    margin-left:30px;
    margin-bottom:300px;
`;

const StyledTable = styled.table`
    border: 3px solid var(--button-hover);
    border-radius: 11px;
    padding: 6px;
`;

export { EditMember };


import React, { useState, useEffect } from 'react';
import styled, { css } from 'styled-components';
import { useParams } from 'react-router-dom';

import { Loading } from '../Loading.jsx';

import { SelectMember } from '../SelectMember.jsx';

import { ToastContainer, toast } from 'react-toastify';

import { 
    CardText, 
    CardHeading, 
    DashboardCard,
    DashboardCardH,
    PageNav, 
    PageNavButton, 
    Page,
    PageNavButtonSelected 
    } from '../DashboardComponents.jsx';

function Detail(props) { 

    let { uuid } = useParams();

    const [transactions,setTransactions] = useState(props.data[1]);
    const [member_detail, setMemberDetail] = useState(props.data[0]);
    const [member_uuid, setMemberUUID] = useState(uuid);

    function removeTransaction(transaction){
        var transaction_id = transaction.transaction_id;
        console.log('removing transaction '+transaction_id)

        const Msg = () => (
            <div>
                <p>
                    <b>Transacion Removed.</b>
                    <br/>Amount: {transaction.amount}
                    <br/>Type: {transaction.type}
                </p>
            </div>
        )

        if(confirm('Are you sure you would like to remove this transaction?\n\n'
            +'Transaction Amount: '+transaction.amount+' RF'
            +'\nFrom: '+transaction.completed)){

            //toast.info("Transaction Removed RF will update shortly.\nRF: "+transaction.amount+"\nTimestamp: "+transaction.completed);

            toast.info(<Msg />)

            //remove actual row from table
            var current_transactions = {'result':this.state.transactions.result}
            var transaction_index = -1;
            
            current_transactions.result.forEach(t => {
                if(t.transaction_id == transaction_id){
                    var index = current_transactions.result.indexOf(t)
                    if (index !== -1) {
                        current_transactions.result.splice(index,1)
                    }
                }
            });

            //send request to the api to remove transaction
            var API_KEY = 'gaiGGD3hpm6cddc67rgf';
            fetch('http://localhost:5000/api/rf_transactions/remove?transaction_id='+transaction_id+'&member_uuid='+this.state.member_uuid+'&api_key='+API_KEY)
                .then(() => {
                    console.log('transaction removed'+transaction_id)
                    this.getAllData()
                });
        }
    }

    if(!transactions || !member_detail){
        return(
            <Page>
            <Loading/>
            </Page>
        );
    }

    var transaction_list = transactions.result.map((transaction) => { 
        return(
            <tr key={transaction.transaction_id}>
                <td><RemoveButton className="rem-button" onClick={() => removeTransaction(transaction)}>x</RemoveButton></td>
                <td>{transaction.amount}</td>
                <td>{transaction.type}</td>
                <td>{transaction.subtype}</td>
                <TDMono>{transaction.completed}</TDMono>
            </tr>
        )
    });

    return (
        <Page>
            <DashboardCardH>
                <div>
                    <BigUserIcon xmlns="http://www.w3.org/2000/svg" className="ionicon" viewBox="0 0 512 512">
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
                    <CardText><b>Rocket Fuel:</b> {member_detail.total_rf}</CardText>
                    <CardText><b>RCL Attendance Credits:</b> {member_detail.rcl_attendance}</CardText>
                    <CardText><b>HQ Points:</b></CardText>
                </div>
            </DashboardCardH>
            {member_detail.parent.name != ''
            ?(<DashboardCard>
                <div>
                    <CardHeading>Member's Parent</CardHeading>
                    <CardText><b>Name:</b> {member_detail.parent.name}</CardText>
                    <CardText><b>Email:</b> {member_detail.parent.email}</CardText>
                    <CardText><b>Phone #:</b> {member_detail.parent.phone}</CardText>
                    <CardText><b>Temp. Password:</b> {member_detail.parent.temp_password}</CardText>
                    <CardText><b>Payment:</b></CardText>
                    <CardText>        Tuition ${member_detail.parent.tuition} - Scholarship ${member_detail.parent.scholarship}</CardText>
                </div>
            </DashboardCard>):(
                <DashboardCard>
                    <CardHeading>Member's Parent</CardHeading>
                    <CardText>Member does not have a parent account</CardText>
                </DashboardCard>
                    )}
            <DashboardCard>
                <div>
                    <TableHeading>Recent RF Transactions</TableHeading>
                    <table id="transaction-table">
                        <thead>
                            <tr>
                                <th></th>
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
                </div>
            </DashboardCard>
        </Page>
    );
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

const StyledTable = styled.table`
    border: 3px solid var(--button-hover);
    border-radius: 11px;
    padding: 6px;
`;

export { Detail };


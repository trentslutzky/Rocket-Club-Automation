import React from 'react';
import ReactDOM from 'react-dom';
import { StaticRouter, BrowserRouter as Router, Switch, Route, useLocation, useHistory, useParams } from 'react-router-dom';
import styled, { css, createGlobalStyle } from 'styled-components';

import { ToastContainer, toast } from 'react-toastify';
import { injectStyle } from "react-toastify/dist/inject-style";


import { SideBar } from './SideBar.jsx';
import { TopBar } from './TopBar.jsx';

import BGImage from '../images/background_1.png';

import { AddMember } from './AddMember.jsx';
import { MemberDetail } from './MemberDetail/MemberDetail.jsx';
import { DashboardHome } from './DashboardHome.jsx';
import { Loading } from './Loading.jsx';
import { SelectMember } from './SelectMember.jsx';

export default function App(){
    injectStyle();
    return (
        <Router>
            <ToastContainer />
            <GlobalStyle/>
                <MainContainer>
                    <TopBar />
                    <PageContainer>
                        <SideBar/>
                        <MainPage>
                            <Switch>
                                <Route exact path="/" component={ DashboardHome }/>
                                <Route path="/add-member" component={ AddMember }/>
                                <Route path="/edit-member/:member_uuid" component={ MemberDetail }/>
                                <Route path="/add-rf" component={ SelectMember }/>
                            </Switch>
                        </MainPage>
                    </PageContainer>
                </MainContainer>
        </Router>
    );
}

const GlobalStyle = createGlobalStyle`
    :root {
        --main-bg:#D0D0D0; 
        --secondary-bg:#FFFFFF;
        --main-foreground:#202020;
        --secondary-foreground:white;
        --accent-0:#375e97;
        --accent-0-darker:#315488;
        --accent-1:#fb6542;
        --accent-2:#ffbb00;
        --accent-3:#3f681c;
        --button-foreground:white;
        --button-foreground-selected:white;
        --button-foreground-not-selected:#dddddd;
        --table-row-select:#F0F0F0;
        --table-border:#a6a6a6;
    }
    body {
        font-size:15px;
        color: black;
        margin: 0px;
        color: var(--main-foreground);
        font-family: 'Montserrat', sans-serif;
        -ms-overflow-style: none;  /* IE and Edge */
        scrollbar-width: none;  /* Firefox */
        &::-webkit-scrollbar {
            display: none;
        }
    }
    table {
        width:100%;
        background-color:var(--secondary-bg);
        font-size:15px;
        border-collapse:collapse;
        border-radius:5px;
    }
    caption{
        font-size: 1.5rem;
        padding: 10px;
        background-color: #ffffff0d;
        border-radius: 12px;
    }
    }
    th, td {
        padding:15px;
    }
    tr {
        border-bottom:1px solid var(--main-bg);
    }
    thead {
        height:50px;
        text-align:left;
        font-size:16px;
        font-weight:bold;
    }

    .Toastify__toast-container--top-right {
        top:75px !important;
    }
    .Toastify__toast--info {
        background-color:var(--accent-0) !important;
    }
`;

const PageContainer = styled.div`
    height:100%;
    width:100vw !important;
    display:flex;
`;

const MainContainer = styled.div`
    height:100%;
    min-height:100vh;
    max-height:100vh;
    display:flex;
    overflow:hidden;
    background:var(--main-bg);
`;

const MainPage = styled.div`
    background:var(--main-bg);
    overflow-x:hidden !important;
    height:100vh;
    width:100%;
    margin-top:65px;
    margin-left:280px;
    display:flex;

    @media(min-width:1800px){
        flex-direction:column;
        align-items:center;
    }
`;

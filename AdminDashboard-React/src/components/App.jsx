import React, {useState, useEffect} from 'react';
import ReactDOM from 'react-dom';
import { StaticRouter, BrowserRouter as Router, Switch, Route, useLocation, useHistory, useParams } from 'react-router-dom';
import styled, { css, createGlobalStyle } from 'styled-components';

import { ToastContainer, toast } from 'react-toastify';
import { injectStyle } from "react-toastify/dist/inject-style";


import { SideBar } from './SideBar.jsx';
import { TopBar } from './TopBar.jsx';

import BGImage from '../images/background_1.png';

import { AddMember } from './AddMember.jsx';
import { Members } from './Members/Members.jsx';
import { DashboardHome } from './DashboardHome.jsx';
import { Loading } from './Loading.jsx';
import { SelectMember } from './SelectMember.jsx';
import { AddRF } from './AddRF.jsx';
import { Login } from './Login.jsx'

export default function App(){
    injectStyle();
        
    const [token, setToken] = useState('test');

    if(!token){
        return( 
            <>
            <GlobalStyle/>
            <Login setToken={setToken}/>
            </>
        );
    }

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
                                <Route path="/members/:uuid" component={ Members }/>
                                <Route path="/members" render={() => <SelectMember dest="members"/>}/>
                                <Route path="/add-rf/:uuid" component={ AddRF }/>
                                <Route path="/add-rf" render={() => <SelectMember dest="add-rf"/>}/>
                                <Route path="/view-database" render={() => <Loading/> }/>
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
    hr{
        width:100%;
        border:none;
        border-bottom:1px solid var(--main-bg);
        margin:0px;
        margin-top:15px;
        margin-bottom:15px;
    }

    form{
        display:flex;
        flex-direction:column;
    }

    input{
        font-family: 'Montserrat', sans-serif;
        border-radius: 4px;
        border: 1px solid var(--main-bg);
        font-size: 16px;
        padding: 8px;
        margin-bottom: 12px;
    }

    label{
        margin-bottom:5px;
        font-size:1rem;
    }

    select{
        font-family: 'Montserrat', sans-serif;
        height: 38px;
        font-size: 1rem;
        padding-left: 3px;
        background-color: var(--secondary-foreground);
        border: 1px solid var(--main-bg);
        border-radius: 3px;
        margin-bottom: 12px;
        cursor:pointer;
        &:hover{
            background-color:var(--table-row-select);
        }
}
    }

    button{
        font-family: 'Montserrat', sans-serif;
        margin-right:25px;
        height: 38px;
        width: 100px;
        margin-top: 15px;
        margin-bottom: 10px;
        background-color: var(--accent-0-darker);
        border: none;
        border-radius: 5px;
        color: var(--secondary-foreground);
        font-size: 1rem;
        cursor: pointer;
        transition: all 0.1s;
        &:hover{
            transform:scale(1.1);
        }
        &:disabled{
            opacity:0.5;
        }
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
    margin-left:250px;
    padding-left:30px;
    display:flex;

    @media(min-width:1800px){
        flex-direction:column;
        align-items:center;
    }

    @media(max-width:1000px){
        margin-left:60px;
    }

    transition:all 0.1s;
`;

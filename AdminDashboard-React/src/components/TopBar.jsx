import React from 'react';
import ReactDOM from 'react-dom';
import { StaticRouter, BrowserRouter as Router, Switch, Route } from 'react-router-dom';
import styled, { css, createGlobalStyle } from 'styled-components';

import RCLogo from '../images/rc_helmet.png';
import AvatarIMG from '../images/rocketclub.png';

class TopBar extends React.Component {

    constructor(props){
        super(props);
    }

    accountClick() {
        const popup = document.getElementById("account-popup");
        console.log(popup.props);
    }

    render(props) {
        return (
            <Bar>
                <Logo src={RCLogo}></Logo>
                <LeftTitle>Rocket Club<br/>Admin Dashboard</LeftTitle>
                <Avatar src={AvatarIMG} onClick={() => this.accountClick()}></Avatar>
                <AccountPopup id="account-popup" opened="False">
                    <h4>Rocket Club Admin</h4>
                    <LogOutLink href="">Log Out</LogOutLink>
                </AccountPopup>
            </Bar>
        );
    }
}

const AccountPopup = styled.div`
    height: 110px;
    width: 175px;
    background-color: var(--secondary-bg);
    position: absolute;
    top: 77px;
    border-radius: 5px;
    padding-left:20px;
    transition 0.5s;
    right:-200px;
`;

const LogOutLink = styled.a`
    position: inherit;
    bottom: 16px;
    right: 16px;
`;

const Logo = styled.img`
    height:60%;
    margin:15px;
`;

const Avatar = styled.img`
    height: 30px;
    width: auto;
    border-radius: 25px;
    border: 3px solid var(--accent-0);
    position: absolute;
    right: 10px;
    background-color: var(--main-bg);
    padding: 5px;
    &:hover{
        background-color: var(--secondary-bg);
    }
    cursor:pointer;
`;

const LeftTitle = styled.p`
    font-size:14px;
    text-align:left;
`;

const Bar = styled.div`
    height:65px;
    background-color:var(--secondary-bg);
    width:100%;
    position:fixed;
    box-shadow:0px 0px 12px -8px #000000;
    display:flex;
    align-items:center;
`;


export { TopBar };

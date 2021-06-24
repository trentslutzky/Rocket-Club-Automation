import React from 'react';
import ReactDOM from 'react-dom';
import { StaticRouter, BrowserRouter as Router, Switch, Route } from 'react-router-dom';
import styled, { css, createGlobalStyle } from 'styled-components';

import RCLogo from '../images/rc_helmet.png';

export function TopBar() {
    return (
        <Bar>
            <Logo src={RCLogo}></Logo>
            <LeftTitle>Rocket Club<br/>Admin Dashboard</LeftTitle>
        </Bar>
    );
}

const Logo = styled.img`
    height:60%;
    margin:15px;
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

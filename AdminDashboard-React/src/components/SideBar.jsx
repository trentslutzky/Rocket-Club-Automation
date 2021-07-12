import React from 'react';
import styled, { css } from 'styled-components';
import { Link } from 'react-router-dom';

import * as SVGIcons from '../images/SVGIcons.jsx';

import RCIcon from '../images/rc_helmet.png';

export function SideBar() {
    return (
        <Side>
            <TopFloatingButton to="/">
                <SVGIcons.HomeIcon />
                <ButtonText>Dashboard</ButtonText>
            </TopFloatingButton>
            <FloatingButton to="/add-member">
                <SVGIcons.UserIcon />
                <ButtonText>Add Member</ButtonText>
            </FloatingButton>
            <FloatingButton to="/members">
                <SVGIcons.EditIcon />
                <ButtonText>Members</ButtonText>
            </FloatingButton>
            <FloatingButton to="/add-rf">
                <SVGIcons.RocketIcon />
                <ButtonText>Add Rocket Fuel</ButtonText>
            </FloatingButton>
            <FloatingButton to="/rcl-dashboard">
                <SVGIcons.CameraIcon />
                <ButtonText>Rocket Club live</ButtonText>
            </FloatingButton>
            <FloatingButton to="/class-dashboard">
                <SVGIcons.BookIcon />
                <ButtonText>Class Rocket Fuel</ButtonText>
            </FloatingButton>
            <FloatingButton to="/reports">
                <SVGIcons.FileIcon />
                <ButtonText>Reports</ButtonText>
            </FloatingButton>
        </Side>
    );
}

const Side = styled.aside`
    height:100vh;
    
    width: 250px;
    
    background-color:var(--accent-0);
    display:flex;
    flex-direction:column;
    color:var(--secondary-foreground);
    overflow-x:hidden;

    margin-top:65px;

    position:fixed;
    z-index:1;

    transition: all 0.1s;

    &:hover{
        width:250px;
    }

    @media(max-width:1000px){
        width:59px;
    }
`;

const ButtonText = styled.p`
    margin-left:20px;
`;

const FloatingButton = styled(Link)`
    display: flex;
    justify-content: left;
    align-items: center;
    text-align:right;
    
    padding-left:18px;

    text-decoration:none;
    color: var(--button-foreground-not-selected);
    &:hover{
        color: var(--button-foreground-selected);
    }

    border-bottom: 1px solid var(--accent-0-darker);
    
    background-color: var(--accent-0);
    
    height:50px;
    
    &:hover {
        background-color:var(--accent-0-darker);
    }
    transform: scale(1);
    transition-duration: 0.2s;

    cursor: pointer;

    -webkit-touch-callout: none; /* iOS Safari */
      -webkit-user-select: none; /* Safari */
       -khtml-user-select: none; /* Konqueror HTML */
         -moz-user-select: none; /* Old versions of Firefox */
          -ms-user-select: none; /* Internet Explorer/Edge */
              user-select: none;
`;

const TopFloatingButton = styled(FloatingButton)`
    paddind-top:3px;
    border-top:1px solid var(--accent-0-darker);
`;

const ButtonIcon = styled.img`
    height: 32px;
    width: 32px;
    margin-right:15px;
    margin-left:-20px;
`;

const HideButton = styled.div`
`;

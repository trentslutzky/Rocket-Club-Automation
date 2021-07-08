import React from 'react';
import styled, { css, keyframes } from 'styled-components';

const fadeInAnimation = keyframes`
    from { opacity:0; }
    to   { opacity:1; }
`;

export const PageTitle = styled.h1`
    margin-bottom:0px;
`;

export const CardText = styled.div`
    margin-bottom:8px;
`;

export const CardHeading = styled(CardText)`
    margin:0px;
    font-size:1.8rem;
    font-weight:bold;
    margin-bottom:10px;
    margin-top:10px;
`;

export const CardSubheading = styled.p`
    font-size:1.3rem;
    margin-top:6px;
    margin-bottom:10px;
`;

export const DashboardCard = styled.div`
    width: 685px;    
    background-color: var(--button-foreground);    
    padding: 19px;    
    padding-bottom: 10px;    
    padding-top: 10px;    
    margin-top: 25px;    
    border-radius: 5px;    
    box-shadow: rgb(0, 0, 0) 0px 0px 12px -8px;    
    height:max-content;
`;

export const DashboardCardH = styled(DashboardCard)`
    display:flex;
    align-items:center;
`;  

export const PageNav = styled.span`
    margin-top:15px;
    display:flex;
    align-items:center;
    margin-bottom:-10px;
    /* animation: ${fadeInAnimation} 0.1s linear; */
`;

export const PageNavButton = styled.button`
    font-size:0.9rem;
    height: 35px;
    width: 192px;
    color: var(--accent-0);
    margin-right: 15px;
    border: 1px solid var(--accent-0-darker);
    background-color: var(--button-foreground-not-selected);
    cursor:pointer;
    border-radius:5px;
    transition: all 0.1s;
    &:hover{
        color: var(--accent-0-darker);
        background-color: var(--button-foreground-selected);
        transform: scale(1.05);
    }
`;

export const Page = styled.div`
    /* animation: ${fadeInAnimation} 0.15s linear; */
    margin-bottom:100px;
    min-width:1000px;
    height:max-content;
`;

export const FieldError = styled.p`
    font-size:0.8rem;
    color:red;
    margin-top: -10px;
    text-align:right;
    margin-bottom:-6px;
`;

export const ListLine = styled.div`
    font-size:15px;
    margin-bottom: -4px;
`;

export const Checkbox = styled.input`
    height:15px;
    width:15px;
    margin-right:10px;
    cursor:pointer;
`;

export const PageNavButtonSelected = styled(PageNavButton)`
    color: var(--button-foreground-not-selected);
    background-color: var(--accent-0);
    cursor:default;
    &:hover{
        color: var(--button-foreground-not-selected);
        background-color: var(--accent-0);
    }
`;

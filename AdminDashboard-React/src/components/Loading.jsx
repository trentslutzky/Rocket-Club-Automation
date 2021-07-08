import React from 'react';
import styled, { css, keyframes } from 'styled-components';
import { Link } from 'react-router-dom';

import loader from '../images/loading-1.gif';

export function Loading() {
    return (
        <Page>
            <LoadingImg src={loader} />
        </Page>
    );
}

const fadeInAnimation = keyframes`
    from { opacity:0; }
    to   { opacity:1; }
`;

const LoadingImg = styled.img`
    height: auto;
    width: 172px;
`;

const Page = styled.div`
    width:100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    margin-top: 259px;
    animation: ${fadeInAnimation} 0.5s cubic-bezier(.65,.05,.36,1);
`;  

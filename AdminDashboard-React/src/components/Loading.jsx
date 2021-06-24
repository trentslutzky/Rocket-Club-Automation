import React from 'react';
import styled, { css } from 'styled-components';
import { Link } from 'react-router-dom';

import loader from '../images/loading-1.gif';

export function Loading() {
    return (
        <Page>
            <LoadingImg src={loader} />
        </Page>
    );
}

const LoadingImg = styled.img`
    height: auto;
    width: 172px;
`;

const Page = styled.div`
    display: flex;
    flex-direction: column;
    align-items: center;
    margin-top: 259px;
`;  

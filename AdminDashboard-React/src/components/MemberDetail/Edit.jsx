import React from 'react';
import styled, { css,keyframes } from 'styled-components';
import { useLocation, useHistory } from 'react-router-dom';

import { Loading } from '../Loading.jsx';
import { CardText, CardHeading, DashboardCard, PageNav, PageNavButton, PageNavButtonSelected, Page } from '../DashboardComponents.jsx';

class Edit extends React.Component { 
    render() {
        return(
        <Page>
            <DashboardCard>
                <CardHeading>Edit Member Info</CardHeading>
                <CardText>Edit Member info in the forms below.</CardText>
            </DashboardCard>
        </Page>
        );
    }
}

export { Edit };


import React from 'react';
import styled, { css } from 'styled-components';
import { useLocation, useHistory } from 'react-router-dom';

import { Loading } from '../Loading.jsx';
import { CardText, CardHeading, DashboardCard, PageNav, PageNavButton, PageNavButtonSelected, Page } from '../DashboardComponents.jsx';

class Certs extends React.Component { 
    render() {
        return(
        <Page>
            <DashboardCard>
                <CardHeading>Awards & Certifications</CardHeading>
                <CardText>update member certs and awards.</CardText>
            </DashboardCard>
        </Page>
        );
    }
}

export { Certs };


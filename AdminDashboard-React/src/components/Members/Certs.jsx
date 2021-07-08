import React, { useState, useEffect } from 'react';
import styled, { css } from 'styled-components';
import { useParams } from 'react-router-dom';

import { toast } from 'react-toastify';

import AjaxLoadnigGif from '../../images/ajax-loader.gif';

import { Loading } from '../Loading.jsx';
import { CardText, 
    CardHeading, 
    CardSubheading, 
    DashboardCard, 
    PageNav, 
    PageNavButton, 
    PageNavButtonSelected, 
    Page, 
    ListLine,
    Checkbox } from '../DashboardComponents.jsx';

function Certs(props) { 

    let { uuid } = useParams();

    const [num_journeys, setNumJourneys] = useState(props.data.journeys.num);
    const [journeys_loading, setJourneysLoading] = useState(false);
    const [journeys_loaded, setJourneysLoaded] = useState(false);

    var memberJourneys = props.data.journeys;

    const [awards_loading, setAwardsLoading] = useState(false);
    const [awards_loaded, setAwardsLoaded] = useState(false);

    var memberAwards = props.data.awards;

    useEffect(() => {
        if(journeys_loading == false){
            setJourneysLoading(true);
            memberJourneys.entre.map((journey) => {
                if(journey.certified){
                    document.getElementById(journey.cert_id).checked = true;
                }
            });
            memberJourneys.science_and_tech.map((journey) => {
                if(journey.certified){
                    document.getElementById(journey.cert_id).checked = true;
                }
            });
            setJourneysLoaded(true);
        }
        if(awards_loading == false){
            setAwardsLoading(true);
            memberAwards.map((award) => {
                if(award.certified == true){
                    document.getElementById(award.id).checked = true;
                }
            });
        }
    })

    var entre_journeys = memberJourneys.entre.map((journey) => {
        return(
            <ListLine key={journey.cert_id}>
                <Checkbox 
                    type="checkbox" 
                    name={journey.cert_id} 
                    onChange={journey_selected}
                    id={journey.cert_id}
                />
                <span>{journey.flair}</span>
            </ListLine>
        )
    });

    var science_journeys = memberJourneys.science_and_tech.map((journey) => {
        return(
            <ListLine key={journey.cert_id}>
                <Checkbox 
                    type="checkbox" 
                    name={journey.cert_id} 
                    onChange={journey_selected}
                    id={journey.cert_id}
                />
                <span>{journey.flair}</span>
            </ListLine>
        )
    });

    var member_awards = memberAwards.map((award) => {
        return(
        <ListLine key={award.id}>
                <Checkbox 
                    type="checkbox" 
                    name={award.id} 
                    onChange={award_selected}
                    id={award.id}
                />
                <span>{award.flair}</span>
        </ListLine>
            )
    })

    function journey_selected(e){
        var value = e.target.checked;
        console.log(value);
        if( value == true ){
            setNumJourneys(num_journeys + 1);
        } else {
            setNumJourneys(num_journeys - 1);
        }
    }

    function award_selected(e){
    }

    function journeySubmit(e){
        document.getElementById("loading-icon-journeys").style.visibility = "visible";
        e.preventDefault();
        var result = []
        for(let i = 0; i < e.target.length -1; i++) {
            result.push([e.target.[i].name,e.target[i].checked]);
        }
        var data = {'member_uuid':uuid,'result':result};
        var API_KEY='gaiGGD3hpm6cddc67rgf';
        var data_json = JSON.stringify(data,null,2);
        fetch('http://192.168.1.188:5000/api/journeys/update?api_key='+API_KEY,{    
            method:'POST',    
            mode:'cors',    
            headers:{'Content-Type': 'application/json'},    
            body:data_json
        }).then((res) => res.json()).then((result) => {
            console.log(result);
            if(result.updated == true){
                props.refresh();
                toast.info('Updated Journeys for '+props.data.name);
            }
            document.getElementById("loading-icon-journeys").style.visibility = "hidden";
        });
    }

    function awardsSubmit(e){
        document.getElementById("loading-icon-awards").style.visibility = "visible";
        e.preventDefault();
        var result = []
        for(let i = 0; i < e.target.length -1; i++) {
            result.push([e.target.[i].name,e.target[i].checked]);
        }
        var data = {'member_uuid':uuid,'result':result};
        var API_KEY='gaiGGD3hpm6cddc67rgf';
        var data_json = JSON.stringify(data,null,2);
        fetch('http://192.168.1.188:5000/api/awards/update?api_key='+API_KEY,{    
            method:'POST',    
            mode:'cors',    
            headers:{'Content-Type': 'application/json'},    
            body:data_json
        }).then((res) => res.json()).then((result) => {
            console.log(result);
            if(result.updated == true){
                props.refresh();
                toast.info('Updated Awards for '+props.data.name);
            }
            document.getElementById("loading-icon-awards").style.visibility = "hidden";
        });
    }

    return(
        <Page>
            <DashboardCard>
                <CardHeading>
                    Member's Journeys ({num_journeys}/24 - {((num_journeys/24)*100).toFixed(1)}%)
                </CardHeading>
                <form onSubmit={journeySubmit}>
                    <CardSubheading>Entrepreneurship and Business</CardSubheading>
                    { entre_journeys }
                    <CardSubheading>Science, Technology, Engineering, and Mathematics</CardSubheading>
                    { science_journeys }
                    <div>
                        <button type="submit">Save</button>
                        <LoadingIcon id="loading-icon-journeys" src={AjaxLoadnigGif} />
                    </div>
                </form>
            </DashboardCard>
            <DashboardCard>
                <CardHeading>Member Awards</CardHeading>
                <form onSubmit={awardsSubmit}>
                    { member_awards }
                    <div>
                        <button type="submit">Save</button>
                        <LoadingIcon id="loading-icon-awards" src={AjaxLoadnigGif} />
                    </div>
                </form>
            </DashboardCard>
        </Page>
    );
}

const LoadingIcon = styled.img`
    visibility:hidden;
`;

export { Certs };


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

import {URL,API_KEY} from '../api.js';

function Certs(props) { 

    let { uuid } = useParams();

    const [num_journeys, setNumJourneys] = useState(props.data.journeys.num);
    const [journeys_loading, setJourneysLoading] = useState(false);
    const [awards_loading, setAwardsLoading] = useState(false);

    var member_data = props.data;

    useEffect(() => {
        if(journeys_loading == false){
            setJourneysLoading(true);
            member_data.journeys.entre.map((journey) => {
                if(journey.certified){
                    document.getElementById(journey.cert_id).checked = true;
                }
            });
            member_data.journeys.science_and_tech.map((journey) => {
                if(journey.certified){
                    document.getElementById(journey.cert_id).checked = true;
                }
            });
        }
        if(awards_loading == false){
            setAwardsLoading(true);
            member_data.awards.map((award) => {
                if(award.certified == true){
                    document.getElementById(award.id).checked = true;
                }
            });
        }
    })

    var entre_journeys = member_data.journeys.entre.map((journey) => {
        return(
            <ListLine key={journey.cert_id}>
                <Checkbox 
                    className="entre"
                    type="checkbox" 
                    name={journey.cert_id} 
                    onChange={journey_selected}
                    id={journey.cert_id}
                />
                <span>{journey.flair}</span>
            </ListLine>
        )
    });

    var science_journeys = member_data.journeys.science_and_tech.map((journey) => {
        return(
            <ListLine key={journey.cert_id}>
                <Checkbox 
                    className="science_and_tech"
                    type="checkbox" 
                    name={journey.cert_id} 
                    onChange={journey_selected}
                    id={journey.cert_id}
                />
                <span>{journey.flair}</span>
            </ListLine>
        )
    });

    var member_awards = member_data.awards.map((award) => {
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
        if( value == true ){
            setNumJourneys(num_journeys + 1);
        } else {
            setNumJourneys(num_journeys - 1);
        }

        var category = e.target.className.split(" ")[2];
        var cert_id = e.target.name;
        var certified = e.target.checked;
        
        var category_journeys = member_data.journeys[category];
        var journey_index = null;
        for(let i = 0; i < category_journeys.length; i++){
            if(category_journeys[i].cert_id == cert_id){
                journey_index = i;
            }
        }
        member_data.journeys[category][journey_index].certified = certified;
    }

    function award_selected(e){
        var award_id = e.target.name;
        var certified = e.target.checked;
        var awards = member_data.awards;
        var award_index = null;
        for(let i = 0; i < awards.length; i++){
            if(awards[i].id == award_id){
                award_index = i;
            }
        }
        member_data.awards[award_index].certified = certified;
    }

    function journeySubmit(e){
        document.getElementById("loading-icon-journeys").style.visibility = "visible";
        document.getElementById("journeys_message").style.visibility = "hidden";
        e.preventDefault();
        var result = []
        for(let i = 0; i < e.target.length -1; i++) {
            result.push([e.target.[i].name,e.target[i].checked]);
        }
        var data = {'member_uuid':uuid,'result':result};
        var data_json = JSON.stringify(data,null,2);
        fetch(URL+'/api/journeys/update?api_key='+API_KEY,{    
            method:'POST',    
            mode:'cors',    
            headers:{'Content-Type': 'application/json'},    
            body:data_json
        }).then((res) => res.json()).then((result) => {
            console.log(result);
            if(result.updated == true){
                props.refresh(member_data);
                toast.info('Updated Journeys for '+props.data.name);
                document.getElementById("journeys_message").innerText = 'Updated.';
            } else {
                document.getElementById("journeys_message").innerText = 'No new updates.';
            }
            document.getElementById("journeys_message").style.visibility = "visible";
            document.getElementById("loading-icon-journeys").style.visibility = "hidden";
        });
    }

    function awardsSubmit(e){
        document.getElementById("loading-icon-awards").style.visibility = "visible";
        document.getElementById("awards_message").style.visibility = "hidden";
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
                props.refresh(member_data);
                toast.info('Updated Awards for '+props.data.name);
                document.getElementById("awards_message").innerText = "Updated.";
            } else {
                document.getElementById("awards_message").innerText = "No new updates.";
            }
            document.getElementById("awards_message").style.visibility = "visible";
            document.getElementById("loading-icon-awards").style.visibility = "hidden";
        });
    }

    return(
        <Page>
            <DashboardCard>
                <CardHeading>
                    Member's Journeys ({num_journeys}/24 - {((num_journeys/24)*100).toFixed(1)}%)
                </CardHeading>
                <form onSubmit={(e) => {console.log(e.target.values);journeySubmit(e)}}>
                    <CardSubheading>Entrepreneurship and Business</CardSubheading>
                    { entre_journeys }
                    <CardSubheading>Science, Technology, Engineering, and Mathematics</CardSubheading>
                    { science_journeys }
                    <div>
                        <button type="submit">Save</button>
                        <LoadingIcon id="loading-icon-journeys" src={AjaxLoadnigGif} />
                        <span id="journeys_message"></span>
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
                        <span id="awards_message"></span>
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


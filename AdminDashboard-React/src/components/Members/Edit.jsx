import React, { useState, useEffect } from 'react';
import styled, { css,keyframes } from 'styled-components';
import { useLocation, useHistory } from 'react-router-dom';

import { ToastContainer, toast } from 'react-toastify';

import { Formik, Form, useField, useFormik, Field, FormikProvider } from 'formik';
import * as Yup from 'yup';
import 'yup-phone';

import Select from 'react-select';

import AjaxLoaderGif from '../../images/ajax-loader.gif';

import { Loading } from '../Loading.jsx';
import { CardText, CardHeading, 
         DashboardCard, PageNav, 
         PageNavButton, PageNavButtonSelected, 
         FieldError,
         Page } from '../DashboardComponents.jsx';

function Edit(props){
    
    const [member_data_state, setMemberData] = useState(props.data[0]);
    const [selectedTeam, setSelectedTeam] = useState(props.data[0].team);
    const [team_options, setTeamOptions] = useState(props.data[1]);

    const [member_info_message, setMemberInfoMessage] = useState('');
    const [parent_info_message, setParentInfoMessage] = useState('');

    var member_info_loading = false;
    var parent_info_loading = false;

    const member_data = props.data[0];

    function updateMemberInfo(info){
        if(!member_info_loading){
            member_info_loading = true;
            document.getElementById("loading-icon-member-detail").style.visibility = "visible";
            var API_KEY = 'gaiGGD3hpm6cddc67rgf';
            fetch('http://192.168.1.188:5000/api/edit/info?api_key='+API_KEY,{
                method:'POST',
                mode:'cors',
                headers:{'Content-Type': 'application/json'},
                body:info
            }).then(res => res.json()).then((result) => {
                console.log(result);
                if(result.updated == true){
                    props.refresh();
                    toast.info('Updated member information for '+member_data.name);
                    setMemberInfoMessage(result.message);
                }
                document.getElementById("loading-icon-member-detail").style.visibility = "hidden";
                member_info_loading = false;
                setMemberInfoMessage(result.message);
            });
        }
    }

    function updateParentInfo(info){
        if(!parent_info_loading){
            parent_info_loading = true;
            document.getElementById("loading-icon-parent").style.visibility = "visible";
            var API_KEY = 'gaiGGD3hpm6cddc67rgf';
            fetch('http://192.168.1.188:5000/api/edit/parent?api_key='+API_KEY,{
                method:'POST',
                mode:'cors',
                headers:{'Content-Type': 'application/json'},
                body:info
            }).then(res => res.json()).then((result) => {
                console.log(result);
                if(result.updated == true){
                    props.refresh();
                    toast.info('Updated '+member_data.name+"'s parent info.");
                    setParentInfoMessage(result.message);
                }
                document.getElementById("loading-icon-parent").style.visibility = "hidden";
                parent_info_loading = false;
                setParentInfoMessage(result.message);
            });
        }
    }

    const MemberDetailForm = () => {
        return(
            <>
                <Formik
                    initialValues={{
                        name:member_data.name,
                        member_id:member_data.member_id,
                        division:member_data.division,
                        team:member_data.team,
                        member_uuid:member_data.member_uuid,
                    }}
                    validationSchema={Yup.object({
                        name: Yup.string()
                            .required('Required')
                            .matches(/^[aA-zZ\s]+$/, "Invalid Name")
                            .trim(),
                        member_id: Yup.number()
                            .required('Required')
                            .integer('Invalid member ID'),
                        division: Yup.number()
                            .required('Required')
                            .integer('Invalid Division'),
                    })}
                    onSubmit={(values) => {
                        console.log('submit member info');
                        member_data.name = values.name;
                        member_data.member_id = values.member_id;
                        member_data.division = values.division;
                        member_data.team = values.team;
                        updateMemberInfo(JSON.stringify(values,null,2));
                    }}
                >
                {(props) => (
                    <Form onSubmit={console.log('test')}>
                        <input
                            type="hidden" 
                            defaultValue={member_data.member_uuid}
                            name="member_uuid"
                        />
                        <label htmlFor="name">Name</label>
                        <input
                            id="name"
                            name="name"
                            type="text"
                            defaultValue={member_data.name}
                            onChange={props.handleChange}
                        />
                        {
                            props.errors.name
                            ? <FieldError>{props.errors.name}</FieldError>
                            : <></> 
                        }
                        <label htmlFor="member_id">Member ID</label>
                        <input
                            id="member_id"
                            name="member_id"
                            type="number"
                            defaultValue={member_data.member_id}
                            onChange={props.handleChange}
                        />
                        {
                            props.errors.member_id
                            ? <FieldError>{props.errors.member_id}</FieldError>
                            : <></> 
                        }
                        <label htmlFor="division">Division</label>
                        <input
                            id="division"
                            name="division"
                            type="number"
                            defaultValue={member_data.division}
                            onChange={props.handleChange}
                        />
                        {
                            props.errors.division
                            ? <FieldError>{props.errors.division}</FieldError>
                            : <></> 
                        }
                        <label htmlFor="team">Team</label>
                        <select name="team"
                            defaultValue={member_data.team}
                            onChange={props.handleChange}
                        >
                            {team_options}
                        </select>
                        {
                            props.errors.team
                            ? <FieldError>{props.errors.team}</FieldError>
                            : <></> 
                        }
                        <div>
                        <button type="submit">Save</button>
                        <LoadingIcon id="loading-icon-member-detail"src={AjaxLoaderGif}/>
                        <span>{ member_info_message }</span>
                        </div>
                    </Form>
                )}
                </Formik>
            </>
        );
    }

    const ParentDetailForm = () => {
        return(
            <>
                <Formik
                    initialValues={{
                        parent_name:member_data.parent.name,
                        email:member_data.parent.email,
                        phone:member_data.parent.phone,
                        tuition:member_data.parent.tuition,
                        scholarshpi:member_data.parent.scholarship,
                    }}
                    validationSchema={Yup.object({
                        parent_name: Yup.string()
                            .required('Required')
                            .matches(/^[aA-zZ\s]+$/, "Invalid Name")
                            .trim(),
                        email: Yup.string()
                            .email('Invalid email.')
                            .required('Required'),
                        phone: Yup.string()
                            .phone('invalid phone number')
                            .required('Required'),
                        tuition: Yup.number()
                            .required('Required'),
                        scholarship: Yup.number()
                            .required('Required')
                    })}
                    onSubmit={(values) => {
                        console.log('submit parent info');
                        member_data.parent.name = values.parent_name;
                        member_data.parent.email = values.email;
                        member_data.parent.phone = values.phone;
                        member_data.parent.tuition = values.tuition;
                        member_data.parent.scholarship = values.tuition;
                        updateParentInfo(JSON.stringify(values,null,2));
                    }}
                >
                {(props) => (
                    <Form onSubmit={props.handleSubmit}>
                        <input
                            type="hidden" 
                            defaultValue={member_data.member_uuid}
                            name="member_uuid"
                        />
                        <label htmlFor="parent_name">Name</label>
                        <input
                            id="parent_name"
                            name="parent_name"
                            type="text"
                            defaultValue={member_data.parent.name}
                            onChange={props.handleChange}
                        />
                        <label htmlFor="email">Email</label>
                        <input
                            id="email"
                            name="email"
                            type="text"
                            defaultValue={member_data.parent.email}
                            onChange={props.handleChange}
                        />
                        <label htmlFor="phone">Phone Number</label>
                        <input
                            id="phone"
                            name="phone"
                            type="text"
                            defaultValue={member_data.parent.phone}
                            onChange={props.handleChange}
                        />
                        <label htmlFor="tuition">Tuition</label>
                        <input
                            id="tuition"
                            name="tuition"
                            type="number"
                            defaultValue={member_data.parent.tuition}
                            onChange={props.handleChange}
                        />
                        <label htmlFor="scholarship">Scholarship</label>
                        <input
                            id="scholarship"
                            name="scholarship"
                            type="number"
                            defaultValue={member_data.parent.scholarship}
                            onChange={props.handleChange}
                        />
                        <div>
                        <button type="submit">Save</button>
                        <LoadingIcon id="loading-icon-parent"src={AjaxLoaderGif}/>
                        <span>{ parent_info_message }</span>
                        </div>
                    </Form>
                )}
                </Formik>
            </>
        );
    }

    return(
        <Page>
            <DashboardCard>
                <CardHeading>Member Details</CardHeading>
                <MemberDetailForm/>
            </DashboardCard>
            <DashboardCard>
                <CardHeading>Parent Details</CardHeading>
                <ParentDetailForm/>
            </DashboardCard>
        </Page>
    );
}

const LoadingIcon = styled.img`
    visibility:hidden;
`;

const ButtonDisabled = styled.button`
    &:hover{
        transform:scale(1.0);
    }
`;

export { Edit };


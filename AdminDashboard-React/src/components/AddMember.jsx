import React, { useState, useEffect } from 'react';
import styled, { css } from 'styled-components';
import { Link } from 'react-router-dom';
import { toast } from 'react-toastify';

import { URL,API_KEY } from './api.js';

import { Formik, Form, useField, useFormik, Field, FormikProvider } from 'formik';    
import * as Yup from 'yup';    
import 'yup-phone';    
    
import Select from 'react-select';    
    
import AjaxLoaderGif from '../images/ajax-loader.gif';    
    
import { Loading } from './Loading.jsx';    
import { CardText, CardHeading,    
         DashboardCard, PageNav,    
         PageNavButton, PageNavButtonSelected,    
         FieldError,    
         Page, PageTitle } from './DashboardComponents.jsx';

export function AddMember() {
    const [pageUpdate, setPageUpdate] = useState(null);
    // stuff for switching sub pages
    const [page_state, setPage] = useState(0);
    
    const [pageData, setPageData] = useState(null);
    const [team_options, setTeamOptions] = useState(    
        <option label="Loading..." defaultValue/>  
    ); 
    const [grad_date_options, setGradDateOptions] = useState(    
        <option label="Loading..." defaultValue/>  
    ); 

    const [addParentAccount, setAddParentAccount] = useState(false);

    useEffect(() => {
        if(pageUpdate == null){
            setPageUpdate(0);
        }
        if(pageData == null){
            // get the page data from the api
            fetch(URL+'/api/add_member/page_data?api_key='+API_KEY,{
                method:'GET',mode:'cors'})
            .then((res) => res.json())
            .then((result) => {
                // do something with the json data from the api
                setPageData(result);
                setTeamOptions( 
                    result.teams.map((team)=>(
                        <option key={team.team_name} value={team.team_name} label={team.team_name}/>
                    ))
                );
                setGradDateOptions( 
                    result.grad_dates.map((g)=>(
                        <option key={g.date} value={g.date} label={g.date}/>
                    ))
                );
            });
        }
    })

    if (pageData == null){
        return(
            <Page>
                <PageTitle>Add Member</PageTitle>
                <Loading/>
            </Page>
        )
    }
    
    function handleAddNormalMember(data){
        document.getElementById("normal-member-loader").style.visibility = 'visible';
        console.log(data);
        fetch(URL+'/api/add_member?api_key='+API_KEY,{
                method:'POST',
                mode:'cors',
                headers:{'Content-Type': 'application/json'},
                body:data
            }).then(res => res.json()).then((result) => {
                console.log(result);
                if(result.updated == true){   
                    toast.info('New Member Added!');
                    setPageData(null);
                }    
                document.getElementById("normal-member-loader").style.visibility = 'hidden';
            });
    }

    function parentAccountSelected(e){
        var height = '0px';
        if(e.target.checked == true){height = '335px';}
        document.getElementById('parent_account_section').style.height = height;
    }

    // use react Formik to create the add member form.
    const AddNormalMemberForm = () => {
        return(
            <>
                <Formik
                    initialValues={{
                        member_id:pageData.upcoming_member_id,
                        add_parent:false,
                        tuition:375,
                        scholarship:0,
                        updater:pageUpdate,
                    }}
                    validationSchema={Yup.object({
                        member_id: Yup.number()
                            .integer('invalid member id')
                            .required('required'),
                        name: Yup.string()
                            .matches(/^[aA-zZ\s]+$/, "Invalid Name")
                            .required('required'),
                        division: Yup.number()
                            .integer('invalid member id')
                            .required('required'),
                        team: Yup.string()
                            .required('required'),
                            grad_date: Yup.string()
                            .required('required'),
                        parent_name: Yup.string()
                            .matches(/^[aA-zZ\s]+$/, "Invalid Name")
                            .when('add_parent', {is:true, then: Yup.string().required('required')}),
                        email: Yup.string()
                            .when('add_parent', {
                                is:true, 
                                then: Yup.string()
                                .email('invalid email')
                                .required('required')}),
                        phone: Yup.string()
                            .when('add_parent', {
                                is:true, 
                                then: Yup.string()
                                .phone('Invalid phone number')
                                .required('required')}),
                        tuition: Yup.number()
                            .when('add_parent', {
                                is:true, 
                                then: Yup.number()
                                .required('required')}),
                        scholarship: Yup.number()
                            .when('add_parent', {
                                is:true, 
                                then: Yup.number()
                                .required('required')}),
                    })}
                    onSubmit={(values) => {
                        handleAddNormalMember(JSON.stringify(values,null,2))
                    }}
                >
                {(props) => (
                    <Form onSubmit={props.handleSubmit}>
                        <label htmlFor="member_id">Member ID</label>
                        <input 
                            id="member_id"
                            name="member_id"
                            type="number"
                            defaultValue={pageData.upcoming_member_id}
                            onChange={props.handleChange}
                        />
                        {
                            props.errors.member_id
                            ? <FieldError>{props.errors.member_id}</FieldError>
                            : <></> 
                        }
                        <label htmlFor="name">Name</label>
                        <input 
                            id="name"
                            name="name"
                            type="text"
                            onChange={props.handleChange}
                        />
                        {
                            props.errors.name
                            ? <FieldError>{props.errors.name}</FieldError>
                            : <></> 
                        }
                        <label htmlFor="division">Division</label>
                        <input 
                            id="division"
                            division="division"
                            type="number"
                            onChange={props.handleChange}
                        />
                        {
                            props.errors.division
                            ? <FieldError>{props.errors.division}</FieldError>
                            : <></> 
                        }
                        <label htmlFor="team">Team</label>
                        <select name="team"
                            onChange={props.handleChange}
                            placeholder=""
                        >
                            <option label="select a team..." disabled selected/>
                            {team_options}
                        </select>
                        {
                            props.errors.team
                            ? <FieldError>{props.errors.team}</FieldError>
                            : <></> 
                        }
                        <label htmlFor="grad_date">Graduation Date</label>
                        <select name="grad_date"
                            onChange={props.handleChange}
                            placeholder=""
                        >
                            <option label="select a graduation date..." disabled selected/>
                            {grad_date_options}
                        </select>
                        {
                            props.errors.grad_date
                            ? <FieldError>{props.errors.grad_date}</FieldError>
                            : <></> 
                        }
                        <div>
                            <input 
                                type="checkbox" 
                                name="add_parent"
                                id="add_parent" 
                                onChange={(e) => {props.handleChange(e);parentAccountSelected(e);}}
                            />
                            <label htmlFor="add_parent">Add Parent Account?</label>
                        </div>
                        <HiddenDiv id="parent_account_section">
                            <CardHeading>Parent Account</CardHeading>
                            <label htmlFor="parent_name">Parent Name</label>
                            <input 
                                id="parent_name"
                                parent_name="parent_name"
                                type="text"
                                onChange={props.handleChange}
                            />
                            {
                                props.errors.parent_name
                                ? <FieldError>{props.errors.parent_name}</FieldError>
                                : <></> 
                            }
                            <label htmlFor="email">Email</label>
                            <input 
                                id="email"
                                email="email"
                                type="text"
                                onChange={props.handleChange}
                            />
                            {
                                props.errors.email
                                ? <FieldError>{props.errors.email}</FieldError>
                                : <></> 
                            }
                            <label htmlFor="phone">Phone Number</label>
                            <input 
                                id="phone"
                                phone="phone"
                                type="text"
                                onChange={props.handleChange}
                            />
                            {
                                props.errors.phone
                                ? <FieldError>{props.errors.phone}</FieldError>
                                : <></> 
                            }
                            <div>
                                <label htmlFor="tuition">Tuition</label>
                                <HInput 
                                    id="tuition"
                                    tuition="tuition"
                                    type="number"
                                    defaultValue={375}
                                    onChange={props.handleChange}
                                />
                                {
                                    props.errors.tuition
                                    ? <FieldError>{props.errors.tuition}</FieldError>
                                    : <></> 
                                }
                                <label htmlFor="scholarship">Scholarship</label>
                                <HInput 
                                    id="scholarship"
                                    scholarship="scholarship"
                                    type="number"
                                    defaultValue={0}
                                    onChange={props.handleChange}
                                />
                                {
                                    props.errors.scholarship
                                    ? <FieldError>{props.errors.scholarship}</FieldError>
                                    : <></> 
                                }
                            </div>
                        </HiddenDiv>
                        <div>
                        {props.isSubmitting
                            ?<></>:<button type="submit">Save</button>}
                        <LoadingIcon id="normal-member-loader"src={AjaxLoaderGif}/>
                        <span></span>
                        </div>
                    </Form>
                )}
                </Formik>
            </>
        )
    }

    function DynamicPage(){
        if(page_state == 0){
            return (
                <>
                <PageNav>
                    <PageNavButtonSelected>Add Member</PageNavButtonSelected>
                    <PageNavButton onClick={() => setPage(1)}>Add Trial Member</PageNavButton>
                </PageNav>
                <DashboardCard>
                    <CardHeading>Add New Member</CardHeading>
                    <AddNormalMemberForm />
                </DashboardCard>
                </>
            );
        }
        if(page_state ==  1){
            return (
                <>
                <PageNav>
                    <PageNavButton onClick={() => setPage(0)}>Add Member</PageNavButton>
                    <PageNavButtonSelected>Add Trial Member</PageNavButtonSelected>
                </PageNav>
                <DashboardCard>
                    <CardHeading>Add Trial Member</CardHeading>
                </DashboardCard>
                </>
            );
        }
    }

    return (
        <Page>
            <PageTitle>Add Member</PageTitle>
            <DynamicPage />
        </Page>
    );
}

const HInput = styled.input`
    width:100px;
    margin-right:25px;
    margin-left:15px;
    margin-top:10px;
`;

const HiddenDiv = styled.div`
    height:0px;
    display:flex;
    flex-direction:column;
    overflow-y:clip;
    transition:all 0.5s;
    border-radius: 5px;
    padding-left: 15px;
    padding-right: 15px;
    background-color: var(--table-row-select);
`;

const LoadingIcon = styled.img`
    visibility:hidden;
`;

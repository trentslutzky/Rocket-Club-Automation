import React, { useState, useEffect } from 'react';    
import styled, { css } from 'styled-components';    
import { useParams } from 'react-router-dom';    
import { toast } from 'react-toastify';    
    
import { URL,API_KEY } from '../api.js';    
    
import { Formik, Form, useField, useFormik, Field, FormikProvider } from 'formik';    
import * as Yup from 'yup';    
import 'yup-phone';    
    
import Select from 'react-select';    
    
import AjaxLoaderGif from '../../images/ajax-loader.gif';    
    
import { Loading } from '../Loading.jsx';    
import { CardText, CardHeading,    
         CardSubheading,
         DashboardCard, PageNav,    
         PageNavButton, PageNavButtonSelected,    
         FieldError,    
         Page, PageTitle } from '../DashboardComponents.jsx';  

export function AddRF() {

    let { uuid } = useParams();

    const [pageData, setPageData] = useState(null);

    const [category_options, setCategoryOptions] = useState(
        <option label="Loading..." selected/>
    );

    const [rcl_options, setRCLOptions] = useState(
        <option label="Loading..." selected/>
    );

    const [communities, setCommunities] = useState(
        <option label="Loading..." selected/>
    );

    const [p,updatePage] = useState(false);

    function updatePageData(){
            fetch(URL+'/api/page_data/add_rf?api_key='+API_KEY,{
                method:'POST',
                mode:'cors',
                headers:{'Content-Type': 'application/json'},
                body:JSON.stringify({'member_uuid':uuid},null,2)
            }).then((res) => res.json()).then((result) => {
                // do something with the json data from the api
                setPageData(result);
            });
    }

    useEffect(() => {
         if(pageData == null){
            // get the page data from the api
            fetch(URL+'/api/page_data/add_rf?api_key='+API_KEY,{
                method:'POST',
                mode:'cors',
                headers:{'Content-Type': 'application/json'},
                body:JSON.stringify({'member_uuid':uuid},null,2)
            }).then((res) => res.json()).then((result) => {
                // do something with the json data from the api
                setPageData(result);
                setCategoryOptions(
                    result.categories.map((c) =>(
                        <option key={c.category} value={c.category} label={c.flair}/>
                    ))
                );
                setRCLOptions(
                    result.rcl_subcategories.map((c) =>(
                        <option key={c.category} value={c.category} label={c.flair}/>
                    ))
                );
                setCommunities(
                    result.communities.result.map((c) =>(
                        <option key={c.name} value={c.name} label={c.community_id}/>
                    ))
                );
            });
        }
    })

    if (pageData == null){
        return(
            <Page>
                <PageTitle>Add Rocket Fuel</PageTitle>
                <Loading/>
            </Page>
        )
    }

    function amountChanged(target){
        var label = document.getElementById('rf-floating-label');
        var num_char = target.value.length;
        var bounds = target.getBoundingClientRect();
        var field_top = bounds.top + 9;
        var field_left = bounds.left + (9.6*num_char) + 15;
        label.style.top=''+field_top+'px';
        label.style.left=''+field_left+'px';
        if(num_char == 0 || num_char > 65){
            label.style.visibility = 'hidden';
        } else {
            label.style.visibility = 'visible';
        }
    }

    function handleSubmit(values,info){
        document.getElementById('submit_button').disabled = true;
        document.getElementById('loading-icon').style.visibility = "visible";
        fetch(URL+'/api/add_rf?api_key='+API_KEY,{    
                method:'POST',    
                mode:'cors',    
                headers:{'Content-Type': 'application/json'},    
                body:info 
            }).then(res => res.json()).then((result) => {
                document.getElementById('submit_button').disabled = false;
                document.getElementById('loading-icon').style.visibility = "hidden";
                if(result.updated == true){
                    updatePage(true);
                    toast.info(values.amount+' RF has been added to the account: '+pageData.member_data.result[0].name);
                } 
                document.getElementById("submit_message").innerText = result.message;
            })
    }

    function categoryChanged(e){
        var subcategory_section = document.getElementById("subcat-section");
        var rcl_optgroup = document.getElementById("rcl-optgroup");
        var com_optgroup = document.getElementById("com-optgroup");
        var subcategory_label = document.getElementById("subcategory_default_option");
        rcl_optgroup.style.display = 'none';
        com_optgroup.style.display = 'none';
        var value = e.target.value;
        if(value == 'rcl' || value == 'communities'){
            subcategory_section.style.visibility = "visible";
        } else {
            subcategory_section.style.visibility = "hidden";
        }

        if(value == 'rcl'){
            rcl_optgroup.style.display = 'block';
            subcategory_label.label = 'select a subcategory...';
        }
        else if(value == 'communities'){
            com_optgroup.style.display = 'block';
            subcategory_label.label = 'select a community...';
        }
    }

    const AddRFForm = () => {
        return(
            <>
                <Formik
                    initialValues={{
                        member_uuid:uuid,
                        subcategory:'',
                    }}
                    validationSchema={Yup.object({
                        category:Yup.string().required('Required'),
                        amount:Yup.number().required('Required')
                    })}
                    onSubmit={(values)=>{
                        handleSubmit(values,JSON.stringify(values,2,null));
                    }}
                >
                {(props) => (
                    <Form>
                        <input 
                            type="hidden" 
                            defaultValue={uuid}
                            name="member_uuid"
                        />
                        <CategoryLine>
                            <CategorySection>
                                <label htmlFor="category">Category</label>
                                <CatSelect 
                                    name="category"    
                                    onChange={(e) => {props.handleChange(e);categoryChanged(e)}}
                                >    
                                    <option label="select a category..." selected disabled/>
                                    {category_options}    
                                </CatSelect>    
                            </CategorySection>
                            <CategorySectionDivider/>
                            <SubCategorySection id="subcat-section">
                                <label id="subcategory_label" htmlFor="subcategory">Subcategory</label>
                                <CatSelect 
                                    name="subcategory"    
                                    onChange={props.handleChange}    
                                >    
                                    <option 
                                        id="subcategory_default_option" 
                                        label="select a subcategory..." 
                                        selected 
                                        disabled
                                    />
                                    <optgroup label="Rocket Club Live" id="rcl-optgroup">
                                        {rcl_options}
                                    </optgroup>
                                    <optgroup label="Communities" id="com-optgroup">
                                        {communities}    
                                    </optgroup>
                                </CatSelect>    
                            </SubCategorySection>
                        </CategoryLine>
                        <label htmlFor="amount">Amount</label>
                        <MonoFloatingLabel id="rf-floating-label"> RF</MonoFloatingLabel>
                        <MonoInput
                            id="amount"
                            name="amount"
                            type="number"
                            placeholder="enter an RF amount..."
                            onChange={(e) => {props.handleChange(e);amountChanged(e.target)}}
                        />
                        <div>
                            <button id="submit_button" type="submit">Add RF</button>
                            <LoadingIcon id="loading-icon"src={AjaxLoaderGif}/>
                            <span id="submit_message"></span>
                        </div>
                    </Form>
                )}
                </Formik>
            </>
        )
    }

    return (
        <Page>
            <h1>Add Rocket Fuel {p}</h1>
            <DashboardCard>
                <CardSubheading>Add Rocket Fuel For</CardSubheading>
                <CardHeading>{pageData.member_data.result[0].name}</CardHeading>
                <AddRFForm/>
            </DashboardCard>
        </Page>
    );
}

const CategoryLine = styled.div`
    display:flex;
`; 

const CategorySection = styled.div`
    display:flex;
    flex-direction:column;
    width:49%;
`;

const SubCategorySection = styled(CategorySection)`
    visibility:hidden;
`;

const CategorySectionDivider = styled.div`
    width:2%
`;

const CatSelect = styled.select`
    margin-top:5px;
    width:100%;
`;

const MonoInput = styled.input`
    font-family: 'IBM Plex Mono', monospace;
`;

const MonoFloatingLabel = styled.label`
    font-family: 'IBM Plex Mono', monospace;
    position:absolute;
    visibility:hidden;
    user-select: none;
    -moz-user-select: none;
    -khtml-user-select: none;
    -webkit-user-select: none;
    -o-user-select: none;
`;

const LoadingIcon = styled.img`
    visibility:hidden;
`;

import React from 'react';
import styled, { css } from 'styled-components';
import { Formik, Form } from 'formik';
import * as Yup from 'yup';

import RCLogo from '../images/rc_helmet.png';

import LoadingIcon from '../images/loading-1.gif';

import { API_KEY,URL } from './api.js';

export function Login(props) {

    function handleSubmit(values){
        console.log(values);
        var login_inputs = document.getElementsByClassName("login_input");
        for (var i = 0; i < login_inputs.length; i++) {
            login_inputs[i].style.visibility = 'hidden';
        }
        document.getElementById("login_loading_icon").style.visibility = 'visible';
        document.getElementById("login_button").disabled = true;
        document.getElementById("login_button").innerText = 'Loading...';
        document.getElementById("error_message").innerText = '';
        fetch(URL+'/api/login?api_key='+API_KEY,{    
                method:'POST',    
                mode:'cors',    
                headers:{'Content-Type': 'application/json'},    
                body:values
        }).then((res)=>res.json()).then((result) => {
            if(result.logged_in == true){
                console.log('logging in!');
                props.setToken({'token':result.token,'role':result.role});
            } else {
                for (var i = 0; i < login_inputs.length; i++) {
                    login_inputs[i].style.visibility = 'visible';
                }
                document.getElementById("login_loading_icon").style.visibility = 'hidden';
                document.getElementById("login_button").disabled = false;
                document.getElementById("login_button").innerText = 'Login';
                document.getElementById("error_message").innerText = result.message;
            }
        })
    }

    const LoginForm = () => {
        return(
            <>
                <Formik
                    initialValues={{
                        username:null,
                        password:null,
                        remember:false,
                    }}
                    validationSchema={Yup.object({
                        username: Yup.string().required('required'),
                        password: Yup.string().required('required')
                    })}
                    onSubmit={(values) => {
                        handleSubmit(JSON.stringify(values,null,2));
                    }}
                >
                {(props) => (
                    <Form>
                        <LoginInput
                            type="text"
                            name="username"
                            id="username"
                            className="login_input"
                            placeholder="username"
                            onChange={props.handleChange}
                        />
                        <LoginInput
                            type="password"
                            name="password"
                            id="password"
                            className="login_input"
                            placeholder="password"
                            onChange={props.handleChange}
                        />
                        <RememberLine>
                            <input 
                                type="checkbox"
                                name="remember"
                                id="remember"
                                className="login_input"
                                onChange={props.handleChange}
                            />
                            <RememberLabel className="login_input" htmlFor="remember">Remember</RememberLabel>
                        </RememberLine>
                        <ErrorMessage id="error_message"></ErrorMessage>
                        <LoginSubmitButton type="submit"
                            id="login_button">
                            Login
                        </LoginSubmitButton>
                    </Form>

                )}
                </Formik>
            </>
        );
    }

    return (
        <Page>
            <LoginCard>
                <LoadingImage id="login_loading_icon" src={LoadingIcon}/>
                <LogoContainer>
                    <RCimg src={RCLogo}></RCimg>
                </LogoContainer>
                <LoginHeading>Rocket Club Admin Dashboard</LoginHeading>
                <LoginForm/>
            </LoginCard>
        </Page>
    );
}

const LoadingImage = styled.img`
    position:absolute;
    top:111px;
    width:150px;
    visibility:hidden;
`;

const Page = styled.div`
    background-color:var(--main-bg);
    height:100vh;
    margin-top:-15px;
    padding-top:200px;
    display:flex;
    flex-direction:column;
    align-items:center;
`;

const LoginCard = styled.div`
    width:100%;
    max-width:330px;
    background-color:var(--secondary-bg);
    border-radius:15px;
    text-align:center;
    box-shadow:2px 2px 5px rgba(0,0,0,0.11);
    padding:15px;
    display:flex;
    flex-direction:column;
    align-items:center;

    @-webkit-keyframes fade-in-bck {
      0% {
        -webkit-transform: translateZ(80px);
                transform: translateZ(80px);
        opacity: 0;
      }
      100% {
        -webkit-transform: translateZ(0);
                transform: translateZ(0);
        opacity: 1;
      }
    }
    @keyframes fade-in-bck {
      0% {
        -webkit-transform: translateZ(80px);
                transform: translateZ(80px);
        opacity: 0;
      }
      100% {
        -webkit-transform: translateZ(0);
                transform: translateZ(0);
        opacity: 1;
      }
    }
	-webkit-animation: fade-in-bck 0.6s cubic-bezier(0.390, 0.575, 0.565, 1.000) both;
	        animation: fade-in-bck 0.6s cubic-bezier(0.390, 0.575, 0.565, 1.000) both;
`;

const LoginInput = styled.input`
    border-radius:0px;
`;

const LoginSubmitButton = styled.button`
    width:100%;
    margin-bottom:35px;
    &:hover{
        transform:scale(1.01);
    }
`;

const LoginHeading = styled.p`
    font-size:1.4rem;
`;

const LogoContainer = styled.div`
    @-webkit-keyframes slide-in-blurred-top {
      0% {
        -webkit-transform: translateY(-1000px) scaleY(2.5) scaleX(0.2);
                transform: translateY(-1000px) scaleY(2.5) scaleX(0.2);
        -webkit-transform-origin: 50% 0%;
                transform-origin: 50% 0%;
        -webkit-filter: blur(40px);
                filter: blur(40px);
        opacity: 0;
      }
      100% {
        -webkit-transform: translateY(0) scaleY(1) scaleX(1);
                transform: translateY(0) scaleY(1) scaleX(1);
        -webkit-transform-origin: 50% 50%;
                transform-origin: 50% 50%;
        -webkit-filter: blur(0);
                filter: blur(0);
        opacity: 1;
      }
    }
    @keyframes slide-in-blurred-top {
      0% {
        -webkit-transform: translateY(-1000px) scaleY(2.5) scaleX(0.2);
                transform: translateY(-1000px) scaleY(2.5) scaleX(0.2);
        -webkit-transform-origin: 50% 0%;
                transform-origin: 50% 0%;
        -webkit-filter: blur(40px);
                filter: blur(40px);
        opacity: 0;
      }
      100% {
        -webkit-transform: translateY(0) scaleY(1) scaleX(1);
                transform: translateY(0) scaleY(1) scaleX(1);
        -webkit-transform-origin: 50% 50%;
                transform-origin: 50% 50%;
        -webkit-filter: blur(0);
                filter: blur(0);
        opacity: 1;
      }
    }

    height: 150px;
    width: 150px;
    border-radius: 75px;
    background: var(--accent-0);
    overflow: clip;
    box-shadow:2px 2px 5px rgba(0,0,0,0.11);
    margin-top:-128px;
	-webkit-animation: slide-in-blurred-top 0.6s cubic-bezier(0.230, 1.000, 0.320, 1.000) both;
	        animation: slide-in-blurred-top 0.6s cubic-bezier(0.230, 1.000, 0.320, 1.000) both;
`;

const RCimg = styled.img`
    height: 83%;
    margin-top: 8px;
    margin-left: 6px;
`;

const RememberLine = styled.div`
    text-align:left;
    margin-bottom:-12px;
    margin-top:10px;
    display:none;
`;

const RememberLabel = styled.label`
    margin-left:8px;
`;

const ErrorMessage = styled.p`
    font-size: 1rem;
    text-align: left;
    margin: 0px;
    margin-top: 10px;
    padding-left: 5px;
    padding-right: 10px;
    color: red;
`;

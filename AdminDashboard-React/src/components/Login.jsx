import React from 'react';
import styled, { css } from 'styled-components';
import { Formik, Form } from 'formik';
import * as Yup from 'yup';

import RCLogo from '../images/rc_helmet.png';

export function Login(props) {

    function handleSubmit(values){
        console.log(values);
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
                            placeholder="username"
                            onChange={props.handleChange}
                        />
                        <LoginInput
                            type="password"
                            name="password"
                            id="password"
                            placeholder="password"
                            onChange={props.handleChange}
                        />
                        <RememberLine>
                            <input 
                                type="checkbox"
                                name="remember"
                                id="remember"
                                onChange={props.handleChange}
                            />
                            <RememberLabel htmlFor="remember">Remember</RememberLabel>
                        </RememberLine>
                        <LoginSubmitButton type="submit">
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
                <LogoContainer>
                    <RCimg src={RCLogo}></RCimg>
                </LogoContainer>
                <LoginHeading>Rocket Club Admin Dashboard</LoginHeading>
                <LoginForm/>
            </LoginCard>
        </Page>
    );
}

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
`;

const RememberLabel = styled.label`
    margin-left:8px;
`;

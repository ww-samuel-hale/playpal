import React, { useState } from 'react';
import './NavBar.css';
import { post } from '../../Utilities/api-utility';
import { NavLink, Link } from 'react-router-dom';

const NavBar = () => {
    const [isLoggedIn, setIsLoggedIn] = useState(false);
    const [showLoginForm, setShowLoginForm] = useState(false);
    const [showRegisterForm, setShowRegisterForm] = useState(false);
    const [loginError, setLoginError] = useState('');
    const [registerError, setRegisterError] = useState('');

    const handleLogout = () => {
        setIsLoggedIn(false);
    };

    const handleLoginClick = () => {
        if (isLoggedIn) {
            handleLogout();
        } else {
            setShowLoginForm(!showLoginForm);
            setShowRegisterForm(false);
            setLoginError(''); // Clear previous error messages
        }
    };

    const handleRegister = () => {
        setShowRegisterForm(!showRegisterForm);
        setShowLoginForm(false);
        setRegisterError(''); // Clear previous error messages
    };

    const submitLogin = async (event) => {
        event.preventDefault();
        const username = event.target.username.value;
        const password = event.target.password.value;
        try {
            await post('/login', { username, password });
            setIsLoggedIn(true);
            setShowLoginForm(false);
            setLoginError('');
        } catch (error) {
            // Assuming the API returns a structured error, you can display a message
            // Adjust based on your API's error structure
            setLoginError(error.response?.data?.message || 'Login failed. Please try again.');
        }
    };
    
    const submitRegister = async (event) => {
        event.preventDefault();
        const username = event.target.username.value;
        const password = event.target.password.value;
        const email = event.target.email.value;
        try {
            await post('/register', { username, email, password });
            setShowRegisterForm(false);
            setRegisterError('');
        } catch (error) {
            // Adjust the error handling based on your API's response structure
            setRegisterError(error.response?.data?.message || 'Registration failed. Please try again.');
        }
    };

    return (
        <nav className="navbar">
            <Link to ="/" className="navbar-logo">
                <div>PlayPal</div>
            </Link>
            <div className="navbar-menu">
                <NavLink to ="/discovery">Discover</NavLink>
                <button onClick={handleLoginClick}>{isLoggedIn ? 'Logout' : 'Log In'}</button>
                {!isLoggedIn && <button onClick={handleRegister}>Register</button>}
            </div>
            {showLoginForm && (
                <div className="login-form-container">
                    <form className="login-form" onSubmit={submitLogin}>
                        <input type="text" placeholder="Username" name="username" required />
                        <input type="password" placeholder="Password" name="password" required />
                        <button type="submit">Login</button>
                        {loginError && <div className="error-message">{loginError}</div>}
                    </form>
                </div>
            )}
            {showRegisterForm && (
                <div className="login-form-container">
                    <form className="login-form" onSubmit={submitRegister}>
                        <input type="text" placeholder="Username" name="username" required />
                        <input type="email" placeholder="Email" name="email" required />
                        <input type="password" placeholder="Password" name="password" required />
                        <button type="submit">Register</button>
                        {registerError && <div className="error-message">{registerError}</div>}
                    </form>
                </div>
            )}
        </nav>
    );
};

export default NavBar;

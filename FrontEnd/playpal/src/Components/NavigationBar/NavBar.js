import React, { useState } from 'react';
import './NavBar.css';
import { post } from '../../Utilities/api-utility';

const NavBar = () => {
    const [isLoggedIn, setIsLoggedIn] = useState(false);
    const [showLoginForm, setShowLoginForm] = useState(false);
    const [showRegisterForm, setShowRegisterForm] = useState(false);

    const handleLogout = () => {
        // Implement logout logic here
        // For example, clear the user token or user state
        setIsLoggedIn(false); // Update the state to reflect that the user is logged out
    };

    const handleLoginClick = () => {
        if (isLoggedIn) {
            handleLogout();
        } else {
            setShowLoginForm(!showLoginForm);
            setShowRegisterForm(false);
        }
    };

    const handleRegister = () => {
        setShowRegisterForm(!showRegisterForm);
        setShowLoginForm(false);
    };

    const submitLogin = async (event) => {
        event.preventDefault();
        const username = event.target.username.value;
        const password = event.target.password.value;
        try {
            const response = await post('/login', { username, password });
            console.log('Login successful:', response);
            setIsLoggedIn(true); // Update the state to reflect that the user is logged in
            setShowLoginForm(false); // Hide the login form
        } catch (error) {
            console.log('Login failed:', error);
        }
    };

    const submitRegister = async (event) => {
        event.preventDefault();
        const username = event.target.username.value;
        const password = event.target.password.value;
        const email = event.target.email.value;
        try {
            const response = await post('/register', { username, email, password });
            console.log('Registration successful:', response);
            setShowRegisterForm(false); // Hide the registration form
        } catch (error) {
            console.log('Registration failed:', error);
        }
    };

    return (
        <nav className="navbar">
            <div className="navbar-logo">PlayPal</div>
            <div className="navbar-menu">
                <button onClick={handleLoginClick}>{isLoggedIn ? 'Logout' : 'Log In'}</button>
                {!isLoggedIn && <button onClick={handleRegister}>Register</button>}
            </div>
            {showLoginForm && (
                <div className="login-form-container">
                    <form className="login-form" onSubmit={submitLogin}>
                        <input type="text" placeholder="Username" name="username" required />
                        <input type="password" placeholder="Password" name="password" required />
                        <button type="submit">Login</button>
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
                    </form>
                </div>
            )}
        </nav>
    );
};

export default NavBar;

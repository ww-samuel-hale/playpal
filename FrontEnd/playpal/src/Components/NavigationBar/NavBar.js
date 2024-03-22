import React, { useState } from 'react';
import './NavBar.css';
import { post } from '../../Utilities/api-utility';

const NavBar = () => {
    const [showLoginForm, setShowLoginForm] = useState(false);

    const handleLogout = () => {
        // Handle logout logic here
    };

    const handleRegister = () => {
        // Handle register logic here
    };

    const handleLogin = () => {
        setShowLoginForm(!showLoginForm);
    };

    const submitLogin = async (event) => {
        event.preventDefault();
        // Implement the login logic here
        var username = event.target.username.value;
        var password = event.target.password.value;
        // and send a POST request to the backend
        try {
            const response = await post('/login', { username, password });
            console.log('Login successful:', response);
        } catch (error) {
            console.log('Login failed:', error);
        }
    };

    return (
        <nav className="navbar">
            <div className="navbar-logo">PlayPal</div>
            <div className="navbar-menu">
                <button onClick={handleLogin}>Log In</button>
                <button onClick={handleRegister}>Register</button>
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
        </nav>
    );
};

export default NavBar;

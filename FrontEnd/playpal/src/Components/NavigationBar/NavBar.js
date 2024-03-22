import React from 'react';
import './NavBar.css';

const NavBar = () => {
    const handleLogin = () => {
        // Handle login logic here
    };

    const handleLogout = () => {
        // Handle logout logic here
    };

    const handleRegister = () => {
        // Handle register logic here
    };

    return (
        <nav className="navbar">
            <div className="navbar-logo">PlayPal</div>
            <div className="navbar-menu">
                <button onClick={handleLogin}>Log In</button>
                <button onClick={handleRegister}>Register</button>
            </div>
        </nav>
    );
};

export default NavBar;

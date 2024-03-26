import React, { useContext, useState } from 'react';
import './NavBar.css';
import { post } from '../../Utilities/api-utility';
import { NavLink, Link, useNavigate } from 'react-router-dom';
import MyContext from '../../Context/Context';

const NavBar = () => {
    const { user, login, logout } = useContext(MyContext);
    const [showLoginForm, setShowLoginForm] = useState(false);
    const [showRegisterForm, setShowRegisterForm] = useState(false);
    const [loginError, setLoginError] = useState('');
    const [registerError, setRegisterError] = useState('');
    const navigate = useNavigate();

    function handleLogout() {
        logout();
        navigate('/');
    };

    const handleLoginClick = () => {
        if (user) {
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
            const response = await post('/login', { username, password });
            login({username: response.username, user_id: response.user_id});
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
                {user && <NavLink to ="/discovery">Discover</NavLink>}
                {user && <NavLink to ="/filters">Filters</NavLink>}
                <button onClick={handleLoginClick}>{user ? 'Logout' : 'Log In'}</button>
                {!user && <button onClick={handleRegister}>Sign up</button>}
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
                        <button type="submit">Sign Up</button>
                        {registerError && <div className="error-message">{registerError}</div>}
                    </form>
                </div>
            )}
        </nav>
    );
};

export default NavBar;

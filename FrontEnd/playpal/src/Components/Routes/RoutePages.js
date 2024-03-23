import React from 'react';
import { Routes, Route } from 'react-router-dom';
import Discovery from '../Discovery/Discovery';
import Home from '../Home/Home';

function RoutePages() {
    return (
        <div className="router-content">
            <Routes>
                <Route path="/" element={<Home />} />
                <Route path="/discovery" element={<Discovery />} />
            </Routes>
        </div>
    );
};

export default RoutePages;

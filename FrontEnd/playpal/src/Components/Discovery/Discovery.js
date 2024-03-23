// Discovery.js
import React, { useState } from 'react';
import GameCard from '../GameCard/GameCard';
import './Discovery.css';
import { get } from '../../Utilities/api-utility';

const Discovery = () => {
    const [games, setGames] = useState([]); // Array of game objects
    const [currentIndex, setCurrentIndex] = useState(0);

    const handleGenerateRecommendations = async () => {
        const recommendations = await get('/recommendation'); // A list of json objects
        setGames(recommendations);
    };

    const handleNext = () => {
        setCurrentIndex((currentIndex + 1) % games.length);
    };

    const handlePrevious = () => {
        setCurrentIndex((currentIndex - 1 + games.length) % games.length);
    };

    return (
        <div className="discovery-container">
            <h1>Welcome to Discovery</h1>
            <button onClick={handleGenerateRecommendations}>Generate Recommendations</button>
            {games.length > 0 && (
                <div className="discovery-navigation">
                    <button onClick={handlePrevious} className="navigation-button">&lt;</button>
                        <div className='game-card-wrapper'>
                            <GameCard game={games[currentIndex]} />
                        </div>
                    <button onClick={handleNext} className='navigation-button'>&gt;</button>
                </div>
            )}
        </div>
    );
};

export default Discovery;

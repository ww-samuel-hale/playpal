import React, { useState, useContext} from 'react';
import GameCard from '../GameCard/GameCard';
import './Discovery.css';
import { post } from '../../Utilities/api-utility';
import MyContext from '../../Context/Context';

const Discovery = () => {
    const { user } = useContext(MyContext);
    const [games, setGames] = useState([]);
    const [currentIndex, setCurrentIndex] = useState(0);
    const [isLoading, setIsLoading] = useState(false); // Loading state

    const handleGenerateRecommendations = async () => {
        setIsLoading(true); // Start loading
        try {
            const recommendations = await post('/recommendation', { user_id: user.user_id });
            setGames(recommendations);
        } catch (error) {
            console.error('Failed to fetch recommendations:', error);
            // Handle error state if necessary
        } finally {
            setIsLoading(false); // End loading
        }
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
            <button onClick={handleGenerateRecommendations} disabled={isLoading}>
                {isLoading ? <div className='spinner'></div> : 'Generate Recommendations'}
            </button>
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

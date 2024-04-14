// GameCard.js
import React, { useState, useEffect, useContext } from 'react';
import './GameCard.css';
import { post } from '../../Utilities/api-utility';
import MyContext from '../../Context/Context';

const GameCard = ({ game }) => {
  const [isSummaryExpanded, setIsSummaryExpanded] = useState(true);
  const summaryThreshold = 250;
  const [isLoading, setIsLoading] = useState(false);
  const { user } = useContext(MyContext);

  const toggleSummary = () => {
    setIsSummaryExpanded(!isSummaryExpanded);
  }

  const handleInteraction = async (interaction) => {
    setIsLoading(true);
    var body = {
      user_id: user.user_id,
      game_id: game.id,
      interaction_type: interaction,
      genre: game.genres,
      rating: game.rating,
      release_date: game.release_date,
      game_modes: game.game_modes,
      themes: game.themes
    }

    try {
      const response = await post('/interaction', body);
      console.log(response);
    } catch (error) {
      console.error('Failed to post interaction:', error);
    } finally {
      setIsLoading(false);
    }
  }

    useEffect(() => {
        if (game.summary.length < summaryThreshold) setIsSummaryExpanded(true);
        else setIsSummaryExpanded(false);
    }, [game]);

  return (
    <div className="game-card">
      <div className="game-card-image-container">
        <img src={game.cover} alt={game.name} />
      </div>
      <h2>{game.name}</h2>
      <div className="summary-container">
        <strong>Summary:</strong>
        <span className="summary-text">
          {isSummaryExpanded ? game.summary : `${game.summary.slice(0, summaryThreshold)}...`}
        </span>
        {game.summary.length > summaryThreshold && (
          <span className="summary-toggle" onClick={toggleSummary}>
            {isSummaryExpanded ? 'Read Less' : 'Read More'}
          </span>
        )}
      </div>
      <p><strong>Rating:</strong> {game.rating}</p>
      <p><strong>Genres:</strong> {game.genres.join(', ')}</p>
      <p><strong>Platforms:</strong> {game.platforms.join(', ')}</p>
      <button onClick={() => handleInteraction('like')} disabled={isLoading}>
        {isLoading ? <div className='spinner'></div> : 'Thumbs Up'}
      </button>
      <button onClick={() => handleInteraction('dislike')}>
        {isLoading ? <div className='spinner'></div> : 'Thumbs Down'}
      </button>
    </div>
  );
};

export default GameCard;

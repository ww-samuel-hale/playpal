// GameCard.js
import React, { useState, useEffect } from 'react';
import './GameCard.css';

const GameCard = ({ game }) => {
  const [isSummaryExpanded, setIsSummaryExpanded] = useState(true);
  const summaryThreshold = 250;

  const toggleSummary = () => {
    setIsSummaryExpanded(!isSummaryExpanded);
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
      <button>Thumbs Up</button>
      <button>Thumbs Down</button>
    </div>
  );
};

export default GameCard;

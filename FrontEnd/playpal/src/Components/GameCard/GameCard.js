// GameCard.js
import React from 'react';
import './GameCard.css';

const GameCard = ({ game }) => {
  return (
    <div className="game-card">
      <div className="game-card-image-container">
        <img src={game.cover} alt={game.name} />
      </div>
      <h2>{game.name}</h2>
      <p>{game.summary}</p>
      <p><strong>Rating:</strong> {game.rating}</p>
      <p><strong>Genres:</strong> {game.genres.join(', ')}</p>
      <p><strong>Platforms:</strong> {game.platforms.join(', ')}</p>
      <button>Thumbs Up</button>
      <button>Thumbs Down</button>
    </div>
  );
};

export default GameCard;

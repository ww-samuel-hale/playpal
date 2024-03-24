import React, { useState } from 'react';
import Select from 'react-select'; 
import './Filters.css';


function formatOptionsForSelect(optionsArray) {
    return optionsArray.map(option => ({
        value: option.toLowerCase().replace(/[\s\W-]+/g, '-'), // Replace spaces and non-word characters with a dash
        label: option // Keep the original string as the label
    }));
}

const Filters = () => {
    const [selectedGenres, setSelectedGenres] = useState([]);
    const [selectedPlatforms, setSelectedPlatforms] = useState([]);
    const [selectedGameModes, setSelectedGameModes] = useState([]);
    const [selectedPlayerPerspectives, setSelectedPlayerPerspectives] = useState([]);
    const [selectedThemes, setSelectedThemes] = useState([]);
    const [selectedReleaseDate, setSelectedReleaseDate] = useState([]);
    const [selectedCompanys, setSelectedCompanys] = useState([]);
    const [selectedAgeRatings, setSelectedAgeRatings] = useState([]);
    const [selectedGameEngines, setSelectedGameEngines] = useState([]);
    const [selectedLanguages, setSelectedLanguages] = useState([]);
    const genresOptions = formatOptionsForSelect(require('./Options.json').genres);
    const platformsOptions = formatOptionsForSelect(require('./Options.json').platforms);
    const gameModesOptions = formatOptionsForSelect(require('./Options.json').game_modes);
    const playerPerspectivesOptions = formatOptionsForSelect(require ('./Options.json').player_perspectives);
    const themesOptions = formatOptionsForSelect(require('./Options.json').themes);
    const releaseDateOptions = [];
    const ageRatingsOptions = [];
    const gameEnginesOptions = formatOptionsForSelect(require('./Options.json').game_engines);
    const languagesOptions = formatOptionsForSelect(require('./Options.json').languages);

    // Handle selection change for each dropdown
    const handleGenreChange = (selectedOptions) => {
        setSelectedGenres(selectedOptions);
    };

    const handlePlatformChange = (selectedOptions) => {
        setSelectedPlatforms(selectedOptions);
    };

    const handleGameModeChange = (selectedOptions) => {
        setSelectedGameModes(selectedOptions);
    };

    const handlePlayerPerspectiveChange = (selectedOptions) => {
        setSelectedPlayerPerspectives(selectedOptions);
    };

    const handleThemeChange = (selectedOptions) => {
        setSelectedThemes(selectedOptions);
    };

    const handleReleaseDateChange = (selectedOptions) => {
        setSelectedReleaseDate(selectedOptions);
    };

    const handleCompanyChange = (selectedOptions) => {
        setSelectedCompanys(selectedOptions);
    };

    const handleAgeRatingChange = (selectedOptions) => {
        setSelectedAgeRatings(selectedOptions);
    };

    const handleGameEngineChange = (selectedOptions) => {
        setSelectedGameEngines(selectedOptions);
    };

    const handleLanguageChange = (selectedOptions) => {
        setSelectedLanguages(selectedOptions);
    };

    return (
        <div className='filters-container'>
            <div className="filters-group">
                <label className='filter-label'>Genres:</label>
                <div className='react-select-container'>
                    <Select
                        isMulti
                        options={genresOptions}
                        onChange={handleGenreChange}
                        value={selectedGenres}
                    />
                </div>
            </div>
            <div className="filters-group">
                <label className='filter-label'>Platforms:</label>
                <div className='react-select-container'>
                    <Select
                        isMulti
                        options={platformsOptions}
                        onChange={handlePlatformChange}
                        value={selectedPlatforms}
                    />
                </div>
            </div>
            <div className="filters-group">
                <label className='filter-label'>Game Modes:</label>
                <div className='react-select-container'>
                    <Select
                        isMulti
                        options={gameModesOptions}
                        onChange={handleGameModeChange}
                        value={selectedGameModes}
                    />
                </div>
            </div>
            <div className="filters-group">
                <label className='filter-label'>Player Perspectives:</label>
                <div className='react-select-container'>
                    <Select
                        isMulti
                        options={playerPerspectivesOptions}
                        onChange={handlePlayerPerspectiveChange}
                        value={selectedPlayerPerspectives}
                    />
                </div>
            </div>
            <div className="filters-group">
                <label className='filter-label'>Themes:</label>
                <div className='react-select-container'>
                    <Select
                        isMulti
                        options={themesOptions}
                        onChange={handleThemeChange}
                        value={selectedThemes}
                    />
                </div>
            </div>
            <div className="filters-group">
                <label className='filter-label'>Release Date:</label>
                <div className='react-select-container'>
                    <Select
                        isMulti
                        options={releaseDateOptions}
                        onChange={handleReleaseDateChange}
                        value={selectedReleaseDate}
                    />
                </div>
            </div>
            <div className="filters-group">
                <label className='filter-label'>Age Ratings:</label>
                <div className='react-select-container'>
                    <Select
                        isMulti
                        options={ageRatingsOptions}
                        onChange={handleAgeRatingChange}
                        value={selectedAgeRatings}
                    />
                </div>
            </div>
            <div className="filters-group">
                <label className='filter-label'>Game Engines:</label>
                <div className='react-select-container'>
                    <Select
                        isMulti
                        options={gameEnginesOptions}
                        onChange={handleGameEngineChange}
                        value={selectedGameEngines}
                    />
                </div>
            </div>
            <div className="filters-group">
                <label className='filter-label'>Languages:</label>
                <div className='react-select-container'>
                    <Select
                        isMulti
                        options={languagesOptions}
                        onChange={handleLanguageChange}
                        value={selectedLanguages}
                    />
                </div>
            </div>
        </div>
    );
};

export default Filters;

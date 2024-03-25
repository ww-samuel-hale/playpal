import React, { useState } from 'react';
import Select from 'react-select'; 
import './Filters.css';

// Helper function to format options for the Select component
function formatOptionsForSelect(optionsArray) {
    return optionsArray.map(option => ({
        value: option.toLowerCase().replace(/[\s\W-]+/g, '-'), // Replace spaces and non-word characters with a dash
        label: option // Keep the original string as the label
    }));
}

// Mapping for age ratings
const age_ratings_mapping = {
    6: 'RP',
    7: 'EC',
    8: 'E',
    9: 'E10',
    10: 'T',
    11: 'M',
    12: 'AO'
};

const Filters = () => {
    // State hooks for each filter category
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

    // Options loaded from JSON files
    const genresOptions = formatOptionsForSelect(require('./Options.json').genres).sort((a, b) => a.label.localeCompare(b.label));
    const platformsOptions = formatOptionsForSelect(require('./Options.json').platforms).sort((a, b) => a.label.localeCompare(b.label));
    const gameModesOptions = formatOptionsForSelect(require('./Options.json').game_modes).sort((a, b) => a.label.localeCompare(b.label));
    const playerPerspectivesOptions = formatOptionsForSelect(require('./Options.json').player_perspectives).sort((a, b) => a.label.localeCompare(b.label));
    const themesOptions = formatOptionsForSelect(require('./Options.json').themes).sort((a, b) => a.label.localeCompare(b.label));
    const ageRatingsOptions = formatOptionsForSelect(Object.values(age_ratings_mapping)).sort((a, b) => a.label.localeCompare(b.label));
    const gameEnginesOptions = formatOptionsForSelect(require('./Options.json').game_engines).sort((a, b) => a.label.localeCompare(b.label));
    const languagesOptions = formatOptionsForSelect(require('./Options.json').languages).sort((a, b) => a.label.localeCompare(b.label));

    // Generating options for release date filters
    const years = Array.from({length: new Date().getFullYear() - 1990}, (_, i) => 1990 + i).reverse();
    const months = Array.from({length: 12}, (_, i) => new Date(0, i).toLocaleString('en-US', {month: 'long'}));
    const releaseDateOptions = [
        ...years.map(year => ({ value: `before-${year}`, label: `Before ${year}` })),
        ...years.map(year => ({ value: `after-${year}`, label: `After ${year}` })),
        ...months.map(month => ({ value: `before-${month}`, label: `Before ${month}` })),
        ...months.map(month => ({ value: `after-${month}`, label: `After ${month}` })),
    ].sort((a, b) => a.label.localeCompare(b.label));

    // Handlers for selection changes in each Select component
    const handleGenreChange = (selectedOptions) => setSelectedGenres(selectedOptions);
    const handlePlatformChange = (selectedOptions) => setSelectedPlatforms(selectedOptions);
    const handleGameModeChange = (selectedOptions) => setSelectedGameModes(selectedOptions);
    const handlePlayerPerspectiveChange = (selectedOptions) => setSelectedPlayerPerspectives(selectedOptions);
    const handleThemeChange = (selectedOptions) => setSelectedThemes(selectedOptions);
    const handleReleaseDateChange = (selectedOptions) => setSelectedReleaseDate(selectedOptions);
    const handleAgeRatingChange = (selectedOptions) => setSelectedAgeRatings(selectedOptions);
    const handleGameEngineChange = (selectedOptions) => setSelectedGameEngines(selectedOptions);
    const handleLanguageChange = (selectedOptions) => setSelectedLanguages(selectedOptions);
    // Function to handle saving the filters
    const handleSaveFilters = async () => {
        const filters = {
            genres: selectedGenres,
            platforms: selectedPlatforms,
            gameModes: selectedGameModes,
            playerPerspectives: selectedPlayerPerspectives,
            themes: selectedThemes,
            releaseDate: selectedReleaseDate,
            ageRatings: selectedAgeRatings,
            gameEngines: selectedGameEngines,
            languages: selectedLanguages,
        };
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
                        isClearable={true}
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
            <button className="save-filters-button" onClick={handleSaveFilters}>
                Save Filters
            </button>
        </div>
    );
};

export default Filters;

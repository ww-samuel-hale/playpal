import './App.css';
import NavBar from './Components/NavigationBar/NavBar';
import RoutePages from './Components/Routes/RoutePages';
import { BrowserRouter } from 'react-router-dom';

function App() {
  return (
    <BrowserRouter>
      <div className="App">
        <NavBar />
        <RoutePages />
      </div>
    </BrowserRouter>
  );
}

export default App;

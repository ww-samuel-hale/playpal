import './App.css';
import NavBar from './Components/NavigationBar/NavBar';
import RoutePages from './Components/Routes/RoutePages';
import { BrowserRouter } from 'react-router-dom';
import { MyProvider } from './Context/Provider';

function App() {
  return (
    <MyProvider>
      <BrowserRouter>
        <div className="App">
          <NavBar />
          <RoutePages />
        </div>
      </BrowserRouter>
    </MyProvider>
  );
}

export default App;

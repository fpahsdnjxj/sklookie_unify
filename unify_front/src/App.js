import './App.css';
import {BrowserRouter} from 'react-router-dom'
import Navbar from './components/Navbar'
import {AppRoutes} from './AppRoutes';
function App() {
  return (
    <BrowserRouter>
    <div className="App">
      <h1>Unify</h1>
      <Navbar/>
      <div id="page-body">
        <AppRoutes/>
      </div>
    </div>
    </BrowserRouter>
  );
}

export default App;

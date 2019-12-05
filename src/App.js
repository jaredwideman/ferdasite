import React from 'react';
import Player from './components/Player'
import SearchBar from './components/SearchBar'
import './App.css';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <SearchBar />
        <Player id="001" name="Jared Wideman" />
        {/* <Player id="002" name="CJ Gray" /> */}
      </header>
    </div>
  );
}

export default App;

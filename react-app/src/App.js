import React, { Component } from 'react';
import './App.css';

import Dashboard from './Dashboard.js';
import FlashMessage from './FlashMessage.js';
import Form from './Form.js';

class App extends Component {
  render() {
    const flashMessages = this.props.flashMessages.map((msg) =>
      <FlashMessage message={msg}/>
    );
    return (
      <div className="App">
        <Dashboard />
        {flashMessages}
        <Form />
        <div className="sep-line-small"><hr /></div>
        <Form />
        <Form />
      </div>
    );
  }
}

export default App;

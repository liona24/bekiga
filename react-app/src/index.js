import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
import registerServiceWorker from './registerServiceWorker';

ReactDOM.render(<App flashMessages={['Hello', 'Lol']}/>, document.getElementById('root'));
registerServiceWorker();

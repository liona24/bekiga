import React, { Component } from 'react';
import './Dashboard.css';

class Dashboard extends Component {
  render() {
    return (
      <div className="Dashboard">
        <div className="Dashboard-float-right">
          <a href="#"  onClick={() => {}}>Logout</a>
        </div>
        <div className="Dashboard-float-left">
          <a href="#" className="symbol" onClick={() => {}}>&#8592;</a>
          <a href="#" className="symbol" onClick={() => {}}>&#8634;</a>
        </div>
      </div>
    );
  }
}

export default Dashboard;

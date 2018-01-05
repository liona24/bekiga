import React, { Component } from 'react';
import './FlashMessage.css';

class FlashMessage extends Component {
  render() {
    return (
      <div className="FlashMessage">
        {this.props.message}
      </div>
    );
  }
}

export default FlashMessage;

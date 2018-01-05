import React, { Component } from 'react';
import './Form.css';

class Form extends Component {
  render() {
    return (
      <form>
        <fieldset>
            <legend>Neues Protokoll anlegen</legend>

            <label for="title">Titel</label>
            <input type="text" id="title" size="30" />

            <label for="type">Typ</label>
            <input type="text" id="type" value="Kindergarten" size="50" />
            
            <label for="for">Objekt</label>
            <input type="text" id="for" size="50" />
            
            <label for="issued_by">Beauftragt von</label>
            <input type="text" id="issued_by" size="50" />

            <label for="date">Datum</label>
            <input type="date" id="date" size="10" />

            <label for="additional_parties">Weitere Teilnehmer</label>
            <input type="text" id="additional_parties" size="50" />

            <input type="button" value="Hinzuf&uuml;gen" onClick={() => alert("LOL")} />
        </fieldset>
      </form>
    );
  }
}

export default Form;

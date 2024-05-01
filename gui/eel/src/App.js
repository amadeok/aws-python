import React, { Component, useEffect } from "react";
import logo from "./logo.svg";
import "./App.css";
import TrackComponent from "./trackComp.js";

import { eel } from "./eel.js";
import { AppProvider } from "./AppContext.js";
import RadioComponent from "./RadioElement.jsx";
import Main from "./Main.jsx";

export var compRef = null;

class App extends Component {
  constructor(props) {
    super(props);
    //    this.componentRef = React.createRef();
    compRef = this

    this.state = {
      track_entries: null,
      upload_attempts: null,
      upload_sites: null,
      count: 0
    };
    eel.set_host("ws://localhost:8888");
    eel.hello("start");

  }
  setCompState(payload) {
    console.log("payload", payload, "comp", compRef);
    try {
      compRef.setState(payload)
    } catch (error) {
      console.log("setCompState error", error);
    }
  }
  pythonAlert(message){
    alert(message)
  }
  
  componentDidMount() {
    window.eel.expose( this.setCompState, 'setCompState' )
    window.eel.expose( this.pythonAlert, 'pythonAlert' )

    eel.get_track_entries()(( payload )  => this.setState( payload ) ) //{track_entries : payload["track_entries"], platforms: payload["upload_sites"] }
    // setTimeout(() => {
    //   console.log("------------- >", this.state)
    // }, 1000);
  }

  componentDidUpdate(prevProps, prevState) {
    console.log('Component updated -', prevProps, prevState);
  }

  render() {
    return (
      <AppProvider>
        <Main compRef={compRef}></Main>
      </AppProvider>

    );
  }
}



export default App;

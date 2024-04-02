import React, { Component, useEffect } from "react";
import logo from "./logo.svg";
import "./App.css";
import TrackComponent from "./trackComp.js";

import { eel } from "./eel.js";
var compRef = null;

class App extends Component {
  constructor(props) {
    super(props);
    //    this.componentRef = React.createRef();

    this.state = {
      track_entries: null, // Example state variable
      count: 0
    };
    eel.set_host("ws://localhost:8888");
    eel.hello();

  }
  setCompState(payload) {
    //console.log("payload", payload, "comp", compRef);
    try {
      compRef.setState(payload)

    } catch (error) {
      console.log("setCompState error", error);
    }
  }
  
  componentDidMount() {
    compRef = this
    window.eel.expose( this.setCompState, 'setCompState' )
    
    eel.get_track_entries()(( payload )  => this.setState( {track_entries : payload } ) )

    console.log('--------------- >Component mounted', this.track_entries, "<-------------");
    // setTimeout(() => {
    //   this.setCompState({track_entries: 32}, this)
    //   setTimeout(() => {
    //     this.setCompState({track_entries: 54}, this)
    //   }, 2000);
    // }, 2000);
  }

  componentDidUpdate(prevProps, prevState) {
    // This code will run after the component updates
    // You can compare previous props and state with current props and state here
    console.log('Component updated -', prevProps, prevState);

  }

  render() {
    const {track_entries, count } = this.state
    return (
      
      <div className="App">
        <header className="App-header">
          <img src={logo} className="App-logo" alt="logo" />
          <h1 className="App-title">Welcome to React {count} </h1>
        </header>
        <p className="App-intro">
          {track_entries && <TrackComponent track={track_entries[0]}></TrackComponent>}
          To get started, edit <code>src/App.js</code> and save to reload.
        </p>
        <div> test</div>
      </div>
    );
  }
}

// const App = () => {
//   useEffect(() => {
//     // This code will run after the component mounts
//     eel.set_host("ws://localhost:8888");
//     eel.hello();

//     // Return a cleanup function if needed
//     return () => {
//       // Cleanup code here if needed
//     };
//   }, []); // Empty dependency array means this effect runs only once after mount

//   return (
//     <div className="App">
//       <header className="App-header">
//         <img src={logo} className="App-logo" alt="logo" />
//         <h1 className="App-title">Welcome to React</h1>
//       </header>
//       <p className="App-intro">
//         To get started, edit <code>src/App.js</code> and save to reload.
//       </p>
//       <div> test</div>
//     </div>
//   );
// };

export default App;

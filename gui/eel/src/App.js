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
      track_entries: null, // Example state variable
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
  
  componentDidMount() {
    window.eel.expose( this.setCompState, 'setCompState' )
    eel.get_track_entries()(( payload )  => this.setState( {track_entries : payload } ) )
  }

  componentDidUpdate(prevProps, prevState) {
    console.log('Component updated -', prevProps, prevState);
  }

  render() {
    return (
      <AppProvider>
        <Main compRef={compRef}></Main>
      {/* <div className="App">
        <header className="_App-header bg-[#222222] text-white min-h-[100px]">
          <h1 className="text-xl _App-title p-2">Upload monitor  </h1>
        </header>
        <div><RadioComponent></RadioComponent></div>
        <div className="App-intro_">
          <div className="flex flex-col">
          {track_entries && track_entries.map((entry, i) => (
            <div key={`${entry["_id"]}${i}`} className="m-5"> 
            <TrackComponent  track={entry}></TrackComponent>
            </div>
          ))}
          </div>

          To get started, edit <code>src/App.js</code> and save to reload.
        </div>
        <div> test</div>
      </div> */}
      </AppProvider>

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

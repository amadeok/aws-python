import React, { useContext } from 'react'
import TrackComponent from './trackComp';
import RadioComponent from './RadioElement';
import { eel } from './eel';
import { useEffect } from 'react';
import { AppContext } from './AppContext';

const Main = ({compRef}) => {

    useEffect(() => {
      return () => {    }
    }, [])
    const { attemptShow, setAttemptShow } = useContext(AppContext);

     const {track_entries, count } = compRef.state
    
    return  (


        <div className="App">
            {/* { <attempComponent></attempComponent>} */}
            {/* <div className=" text-white p-[150px]">dawdsas</div> */}
            <header className="_App-header bg-[#222222] text-white _min-h-[100px]">
                <h1 className="text-xl _App-title p-2">Upload monitor  </h1>
            </header>
            <div className=" bg-[#222222] text-white flex px-5 pb-2 _min-h-[100px]">
                <div> <RadioComponent label={"Display attemps:"} style={'flex flex items-start '} selectedOption={attemptShow} setSelectedOption={setAttemptShow} values={["None", "Error", "All"]}></RadioComponent></div> 
                 {/* {attemptShow} */}
            </div>
            <div className="App-intro_">
                <div className="flex flex-col">
                    {track_entries && track_entries.map((entry, i) => (
                        <div key={`${entry["_id"]}${i}`} className="m-5">
                            <TrackComponent track={entry}></TrackComponent>
                        </div>
                    ))}
                </div>
                {/* {track_entries && <TrackComponent track={track_entries[0]}></TrackComponent>} */}
                {/* {track_entries && <TrackComponent2 attempt={track_entries[0]["uploads"]["youtube"]["upload_attempts"][0]}></TrackComponent2>} */}

                To get started, edit <code>src/App.js</code> and save to reload.
            </div>
            <div> test</div>
        </div>

    );
}



export default Main
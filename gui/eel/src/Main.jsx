import React, { useContext } from 'react'
import TrackComponent from './trackComp';
import RadioComponent from './RadioElement';
import { eel } from './eel';
import { useEffect, useState, useRef } from 'react';
import { AppContext } from './AppContext';
import DropdownComponent from './DropdownComp';
import UploadSessionComponent from './UploadSessionComp';
import CheckboxComponent from './CheckboxComponent';

import _ from 'lodash';
import { formatDate } from './utils';
import BarsChart from './BarsInfoCharComp';



const Main = ({ compRef }) => {

   // const [scrollPosition, setScrollPosition] = useState(0);
   const scrollPosition = useRef({})
   const curScrollPosition = useRef(0)

   const pages = ["Track monitor", "Sessions monitor"]
   const [showing, setShowing] = useState("Track monitor")
   // const showingRef = useRef(showing)
   const showingDisable = useRef(false)
   const {showingRef, prevShowingRef } = useContext(AppContext);
   const { track_entries, upload_sessions, count } = compRef.state
   const sessionRef = useRef()
   const tracksRef = useRef()
   const prevT = useRef(null)
   const [selectedTrack, setSelectedTrack] = useState(null)
   const [selectedSession, setSelectedSession] = useState(null)

   const [scrollPosState, setScrollPosState] = useState(scrollPosition.current)
   const [curScroll, setCurScroll] = useState(0)
   const [showIds, setShowIds] = useState(false)
   const [attemptShow, setAttemptShow] = useState('All'); //None, Error, All
   const [HL, setHL] = useState(null)
   const ctx = { attemptShow: attemptShow, showIds: showIds, selectedTrack: selectedTrack, selectedSession: selectedSession, HL:HL, setHL:setHL }


   const handleScroll = (type) => {
      let tryn = 0
      let t1 = new Date().getTime()
      let lastScrollY = window.scrollY;
      function checkScroll() {
         if (window.scrollY !== lastScrollY) {
            // console.log("Window scrolled!", new Date().getTime() - t1, "| ", window.scrollY, " | ", lastScrollY);
            lastScrollY = window.scrollY; // Update lastScrollY
            scrollPosition.current[type] = window.scrollY
            console.log("---------- >", scrollPosition.current["Track monitor"], scrollPosition.current["Sessions monitor"], window.scrollY)

         } else if (tryn++ < 20)
            setTimeout(checkScroll, 10); // Adjust delay as needed
         else console.log("Window scroll timeout", new Date().getTime() - t1, "| ", window.scrollY, " | ", lastScrollY);
      }
      checkScroll();
   };

   useEffect(() => {
      const handleScroll = (e) => {
         const position = window.scrollY;
         curScrollPosition.current = position
         scrollPosition.current[tracksRef.current ? pages[0] : pages[1]] = position
         //  console.log("useEffect---------->",  curScrollPosition.current, "t", scrollPosition.current[pages[0]] ,  "s",scrollPosition.current[pages[1]] )
      };
      window.addEventListener('scroll', handleScroll);
      for (let i = 0; i < pages.length; i++) {
         const page = pages[i];
         scrollPosition.current[page] = 0;
         scrollPosState[page] = 0
      }
      console.log("scrollPosition.current", scrollPosition.current)
      return () => { window.removeEventListener('scroll', handleScroll); };
   }, []);

   useEffect(() => {
      const showing = localStorage.getItem('showing');
      if (showing) setShowing(showing);

      const selectedTrack = localStorage.getItem('selectedTrack');
      if (selectedTrack) setSelectedTrack(selectedTrack)

      const selectedSession = localStorage.getItem('selectedSession');
      if (selectedSession) setSelectedSession(selectedSession)

      const bDisplayAttempts = localStorage.getItem('attemptShow');
      if (bDisplayAttempts) setAttemptShow(bDisplayAttempts);

      const bshowids = localStorage.getItem('bshowids');
      if (bshowids) setShowIds(bshowids);

      return () => { }
   }, [])

   useEffect(() => {
      showingRef.current = showing
      return () => {
      }
   }, [showing])

   const handleSelectChange = (event) => {
      const id = track_entries && track_entries[event.target.selectedIndex - 1]._id//.find(item => item._id ===  selectedTrack)
      // console.log("...->event.target.selectedIndex", event.target.selectedIndex, track_entries[event.target.selectedIndex-1].track_title);
      if (id) {
         setSelectedTrack(id);
         if (localStorage)
            localStorage.setItem("selectedTrack", id)
      }
   }
   const handleSelectChangeSession = (event) => {

      const id = upload_sessions && upload_sessions[event.target.selectedIndex - 1]._id
      console.log("----------.-.-", id)

      if (id) {
         setSelectedSession(id);
         if (localStorage)
            localStorage.setItem("selectedSession", id)
      }
   }
   const handlePageSwitch = (page) => {
      const prev = _.cloneDeep(showingRef.current)
      const prev_pos = _.cloneDeep( scrollPosition.current[prev])
      const cur = _.cloneDeep( page)
      const cur_pos = _.cloneDeep( scrollPosition.current[cur])
      // console.log("...........", "prev", prev, " | prev_pos", prev_pos, " | cur", cur, " | cur_pos", cur_pos," | showingRef.current",  showingRef.current  )
      showingRef.current = page
      setTimeout(() => {
         // console.log("...........", "prev", prev, " | prev_pos", prev_pos, " | cur", cur, " | cur_pos", cur_pos," | showingRef.current",  showingRef.current  )
         window.scrollTo({     top: cur_pos,     behavior: 'instant'    });
      }, 100);

      setShowing(page);

      if (localStorage)
         localStorage.setItem("showing", page)
   }
   // useEffect(() => {
   //    showingDisable.current = true
   //    setTimeout(() => {
   //       showingDisable.current = false
   //    }, 0);

      
   //    // if (pos)
   //    setTimeout(() => {
   //       const pos = scrollPosition.current[showingRef.current]

   //       if (1)

   //          window.scrollTo({
   //             top: pos,
   //             behavior: 'smooth' // Optionally, you can use 'auto' for instant scrolling
   //          });
   //    }, 50);
   //    // prevShowingRef
   //    // console.log("-------> useEffect showingref ", showing,pos)
   // }, [showingRef.current])

   const store = (name, obj) =>{
      if (localStorage)localStorage.setItem(name, obj)
   }
   
   return (

      <div className="_App">
         <header id='fixed-menu' className="_App-header bg-[#222222] text-white _min-h-[100px] text-center _mx-auto items-center justify-center flex flex-col">
            <div className='flex items-center p-2'>
               {/* <div>{curScroll}</div> */}

               {pages.map((page, i) =>
                  <div key={i}>
                     <button onClick={() => handlePageSwitch(page)}
                        className={` _cursor-pointer text-xl _App-title p-2 m-2 rounded-xl ${page === showing ? " border bg-[#333] " : ""}`}  >{page}   </button>
                     {scrollPosState[page]}
                  </div>

               )}
            </div>
            <div className="flex bg-[#222222] text-white px-3 items-center">
               {showing === "Track monitor" ?
                  <div className='flex items-center'>
                     <button onClick={create_track_entry}
                        className="button1 mx-2">New track</button>
                     {sessionDropdown()}
                  </div>

                  :
                  <div className='flex items-center'>
                     <button onClick={() => eel.create_entry({ "date": new Date(), "pre_upload_errors": [], "upload_attempts": [], "track_ids": [], "collection": "upload_sessions" })} 
                     className="button1 mx-2">New upload session</button>

                     {/* {sessionDropdown()} */}

                     <DropdownComponent label={"Current Track"} placeholder={getPlaceholder()} options={track_entries && track_entries.map((e) => ({ id_: e._id, label: e.track_title }))}
                        selectedOption={selectedTrack} handleSelectChange={handleSelectChange} ></DropdownComponent>

                     <div className='bg-[#222] px-3'> Show Ids <input type="checkbox" checked={showIds}
                        onChange={(event) => { setShowIds(event.target.checked); store("showIds", event.target.checked); console.log("event.target.checked", event.target.checked) }} /></div>
                  </div>
               }

               <div className='px-2'> <RadioComponent label={"Display attemps:"} style={'flex flex items-start '} selectedOption={attemptShow} setSelectedOption={(e) => { store("attemptShow", e.target.value); console.log(e.target.value); setAttemptShow(e.target.value) }} values={["None", "Error", "All"]}></RadioComponent></div>
               {/* </div> */}
            </div>
         </header>
         {HL && <div className='absolute z-40 bg-slate-500 rounded-xl p-3 py-1'>{HL}</div>}
         
         <div class="spacer">
            &nbsp;
         </div>
         {/* <div className='fixed-menu'>FIXED</div> */}


         {showing === "Track monitor" ?
            // <TrackMonitor compRef={compRef}>                </TrackMonitor> 
            <div className="App-intro_">
               <div className="flex flex-col _h-full _overflow-y-scroll "  ref={tracksRef}> 
               {/* onWheel={()=>handleScroll("Track monitor")}> */}
                  {track_entries && track_entries.map((entry, i) => (
                     <div key={`${entry["_id"]}_${i}`} className="m-5">
                        <TrackComponent track={entry} ctx={ctx}></TrackComponent>
                     </div>
                  ))}
               </div>
            </div>
            :
            <div className="App-intro_"  >
               <div className="flex flex-col _h-full  _overflow-y-scroll" ref={sessionRef} >
                  {/* onWheel={()=>handleScroll("Sessions monitor")}> */}
                  {upload_sessions && upload_sessions.map((session, i) => (
                     <div key={`${session["_id"]}_${i}`} className="m-5">
                        <UploadSessionComponent uploadSession={session} ctx={ctx}></UploadSessionComponent>
                     </div>
                  ))}
               </div>
            </div>
         }


         {/* {showing === "Track monitor" ? <TrackMonitor compRef={compRef}></TrackMonitor> : <div></div>} */}

      </div>
   )

   function create_track_entry() {
      const number = track_entries ? track_entries.length : 0
      const file_details = {"file_path": "C:\\Users\\amade\\Documents\\dawd\\lofi1\\lofi\\Mixdown\\output\\None_00024v2_s\\__00024v2_s_joined.mp4", 
      "bpm": 119,  "bars": 16, "bars_per_template": 2, "beats_per_bar": 4, "avee_custom_lenghts": {"0": {"dur":2}}}
      eel.create_entry({ "track_title": `New track${number}`, "op_number": number, "grade": "b", "for_distrokid": false,  
      "entry_status": "pending", "upload_attempts": [], "file_details":file_details, "collection": "track_entries" });
   }

   function sessionDropdown() {
      return <DropdownComponent label={"Current Session"} placeholder={getPlaceholderSession()} options={upload_sessions && upload_sessions.map((e, i) => ({ id_: e._id, label:  `${formatDate(new Date(e.date))} (${i})` }))}
         selectedOption={selectedSession} handleSelectChange={handleSelectChangeSession}></DropdownComponent>;
   }

   function getPlaceholder() {
      let ph = track_entries && track_entries.find(item => item._id === selectedTrack)
      if (ph) return ph.track_title
      else {   // setSelectedTrack("NOT_FOUND")
         return "NOT_FOUND"
      }
   }
   function getPlaceholderSession() {
      let ph = null
      var i = 0
      if (upload_sessions)
      for (i = 0; i <  upload_sessions.length; i++){
         if (upload_sessions[i]._id === selectedSession){
            ph = upload_sessions[i]
            break
         }
      }
      //let ph = upload_sessions && upload_sessions.find(item => item._id === selectedSession)
      if (ph) return `${formatDate(new Date(ph.date))} (${i})`
      else {   // setSelectedTrack("NOT_FOUND")
         return "NOT_FOUND"
      }
   }
   //  (


}



export default Main
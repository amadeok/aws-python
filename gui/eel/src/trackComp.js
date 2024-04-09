
import { useState, useEffect } from "react";
import EditableText from "./EditableText";
import DatePickerComponent2 from "./DatePickerText2";
import DatePickerComponent from "./DatePickerText";

import CheckboxComponent from "./CheckboxComponent";
//import uploadAttempComponent from "./uploadAttempComp";
// import TrackComponent2 from "./attempComp";
import AttemptUploadComponent from "./AttemptUploadComponent";
import { compRef } from "./App";
import { eel } from "./eel";
import { AppContext } from './AppContext';
import { useContext } from "react";
import { formatDate } from "./utils";

const TrackComponent = ({ track, ctx }) => {

  const { } = useContext(AppContext);
  // console.log("theme", attemptShow)
  const { _id, track_title, grade, for_distrokid, upload_attempts, entry_status } = track;

  const {attemptShow, showIds,  selectedTrack, selectedSession } = ctx

  useEffect(() => {
      // console.log("------------------->", upload_attempts, upload_attempts.filter(obj => obj.site === "threads"))
  }, [track])

  // Object.keys(uploads).map((platform) => (
  //   console.log("----------->", uploads, uploads[platform].upload_attempts)
  // ))
  const {upload_sites} = compRef.state
  function setter(t) {
    // compRef.setState({"track_title": t})
    track.track_title = t
    console.log("------------------->setter", track.track_title, track)
  }
  const isInArray = (string, array) => array.includes(string);

  const platformN = upload_sites.length
  const platformPerc = 100/platformN
  const Styles = "_grow _w-[20%] flex-1 text-left border rounded-xl mx-2 p-2 py-1 border-[#707070] " 
  return (
    <div className="text-[#bebebe] text-center">
      <div className="flex _grow   justify-evenly">
        <h2 className="_my-3 p-1 ">Track Details: </h2>
        {/* <EditableText initialValue={"test"} ></EditableText> */}
        <EditableText label={"Track Title:"} value={track_title} style={Styles}
          path={{ "_id": _id, "path": "track_title", "index": null, "field": null , "collection": "track_entries" }}>
        </EditableText>
        <EditableText label={"Grade:"} value={grade} style={Styles}
          path={{ "_id": _id, "path": "grade", "index": null, "field": null, "collection": "track_entries" }}>
        </EditableText>
        <CheckboxComponent label={"For DistroKid:"} value={for_distrokid} style={Styles}
          path={{ "_id": _id, "path": "for_distrokid", "index": null, "field": null, "collection": "track_entries" }}
        ></CheckboxComponent>

        <EditableText label={" Entry status:"} value={entry_status} style={`${Styles}  outline  font-semibold ${entry_status == "ready" ? " text-[#ffffff]  bg-green-800 outline-1  outline-[#00ff00] " : " text-[#000000] bg-yellow-200  outline-[#ff0000] " }`}  path={{ "_id": _id, "path": "entry_status", "index": null, "field": null, "collection": "track_entries" }} validator={(text) => { console.log("validator", text); const arr = ["ready", "pending", "error"]; return isInArray(text, arr) ? null : `${text} not in ${arr}` }}>
        </EditableText>
        {/* <p className={Styles}  >For DistroKid: {for_distrokid.toString()}</p> */}

      </div>
      { (attemptShow !== "None" && true) &&
      <div className="mt-3 border rounded-xl border-[#707070] p-2">
        <h3>Uploads</h3>
        {/* Rendering upload details for each platform */}
        <ul className="_grid _grid-flow-col _auto-cols-max flex justify-start flex-wrap">
          {upload_sites.map((platform, i) => (
            // uploads[platform].upload_attempts.length || 1
            true ?
              <div key={`${platform}_${_id}_${i}`} className={` ${i < platformN - 1 ? "border-r" : ""} w-[50%] md:w-[14.28%] _flex-[0.1] px-2 border-[#707070] `}>
                {/* <ul > */}
                  <div className="flex flex-col  _bg-red-200  _w-[30%]">
                    {platformElem(platform)} 
                  
                    {upload_attempts  && upload_attempts.filter(obj => obj.site === platform).map((attempt, i) => attempt.error.length ||  attemptShow === "All" ? 
                    (
                       <div key={`${i}_platform`} className={`flex text-[#bebebe] text-left pl-2 _px-2 _py-1 my-[2px] border ${ attempt.error.length ? "border-[#ff0000] _border-[5px]" : "border-[#707070]"}  rounded-xl justify-between`}>
                       <div  className="_grow">
                          
                         <DatePickerComponent label={"Date:"} value={attempt.date} style={""}
                          path={{ "_id": attempt._id, "path": "date", "index": null, "field": null, "collection": "upload_attempts" }}>
                         </DatePickerComponent>

                         <EditableText label={"Error:"} value={attempt.error} style={""}
                          path={{ "_id": attempt._id, "path": "error", "index": null, "field": null, "collection": "upload_attempts" }}> </EditableText>
                       </div>
                       <div onClick={()=> eel.delete_entry({ "_id": attempt._id, "collection": "upload_attempts" } )} 
                        className=" cursor-pointer bg-red-500 w-[7px] rounded-r-xl ml-2"></div>

                     </div>
                    //  <div key={`${i}_platform`}>

                    //   </div>

                    ) 
                    : <div key={`${i}_platform`}></div> )}
                  </div>
                {/* </ul> */}
              </div>
              : <div key={`${platform}_${_id}`} ></div>
          ))}
        </ul>
        </div>
      }
      <div className="flex justify-center mt-3">
        {_id}
        <button onClick={()=> eel.delete_entry({ "_id": _id,"collection": "track_entries"} ) } className="mx-5 px-3 border rounded-xl">Delete track entry</button>
      </div>
      
    </div>
  );

  function getSessionDate(session_entry_id) {
    const ret = compRef.state.upload_sessions.find(item => item._id === session_entry_id)
    return ret ? formatDate(new Date(ret.date)) : "session not found";
  }

  function platformElem(platform) {
    return <div className=" text-center"> {platform}:
      <div
         onClick={() => {if (!compRef.state.upload_sessions.length || getSessionDate(selectedSession) == "session not found") alert("No upload session "); else
          eel.create_entry({ "track_entry_id": _id, "session_entry_id": selectedSession, "site": platform, "date": new Date(), "error":"", "collection": "upload_attempts" })}} 
        // onClick={() => eel.add_field({ "_id": _id, "path": `uploads.${platform}.upload_attempts`, "field": null, "value": {"site": platform, "date": "", "error": "" } })}
        
        className="inline ml-1 border border-[#909090] rounded-xl px-1 _h-[20px] cursor-pointer">+</div>
    </div>;
  }
};

export default TrackComponent;
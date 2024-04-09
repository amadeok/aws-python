
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

const UploadSessionComponent = ({ uploadSession, ctx }) => {

  const {  } = useContext(AppContext);
  
  const { _id, date, pre_upload_errors, upload_attempts, track_ids , selectedSession} = uploadSession;
   const {attemptShow, showIds,  selectedTrack } = ctx

  setTimeout(() => {
    console.log("UploadSessionComponent", uploadSession, selectedTrack, "|", showIds)  
  }, 200);
  

  const {upload_sites} = compRef.state

  const isInArray = (string, array) => array.includes(string);

  const platformN = upload_sites.length
  const platformPerc = 100/platformN
  const Styles = "_grow _w-[20%] flex-1 text-left border rounded-xl mx-2 p-2 py-1 border-[#707070] " 
  return (
    <div className={`text-[#bebebe] text-center ${attemptShow !== "None" ? "" : "flex items-center"}`}>
      <div className="flex _grow   justify-evenly items-center">
        <h2 className="_my-3 p-1 ">Sessions Details: </h2>

        <div className=" border border-[#707070] rounded-xl px-2 mx-2" >  <DatePickerComponent  label={"Date:"} value={date} style={""}
          path={{ "_id": _id, "path": "date", "index": null, "field": null, "collection": "upload_sessions" }}> </DatePickerComponent>  </div>

        <div className="flex grow  _py-1 items-center border rounded-xl px-2 h-fit border-[#707070] ">
          <span className="pr-2">Track ids: </span>
          {track_ids && track_ids.map((id, i) =>
            <div key={i} className="flex flex-col text-[14px] _border _rounded-xl border-[#707070] px-2 h-fit border-l">
              <div>  {compRef.state.track_entries.find(item => item._id === id)?.track_title}   {showIds && <div className="text-[11px]"> {`${id}`}</div>} </div>
            </div>)}
        </div>
        {/* <EditableText label={"Grade:"} value={grade} style={Styles}
          path={{ "_id": _id, "path": "grade", "index": null, "field": null, "collection": "track_entries" }}>
        </EditableText>
        <CheckboxComponent label={"For DistroKid:"} value={for_distrokid} style={Styles}
          path={{ "_id": _id, "path": "for_distrokid", "index": null, "field": null, "collection": "track_entries" }}
        ></CheckboxComponent>

        <EditableText label={" Entry status:"} value={entry_status} style={`${Styles}  outline  font-semibold ${entry_status == "ready" ? " text-[#ffffff]  bg-green-800 outline-1  outline-[#00ff00] " : " text-[#000000] bg-yellow-200  outline-[#ff0000] " }`}  path={{ "_id": _id, "path": "entry_status", "index": null, "field": null, "collection": "track_entries" }} validator={(text) => { console.log("validator", text); const arr = ["ready", "pending", "error"]; return isInArray(text, arr) ? null : `${text} not in ${arr}` }}>
        </EditableText> */}
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
                  
                    {upload_attempts && upload_attempts.filter(obj => obj.site === platform).map((attempt, i) => attempt.error.length ||  attemptShow === "All" ? (
                      <div key={`${i}_platform`} className={`flex text-[#bebebe] text-left pl-2 _px-2 _py-1 my-[2px] border ${ attempt.error.length ? "border-[#ff0000] _border-[5px]" : "border-[#707070]"}  rounded-xl justify-between`}>
                        <div  className="_grow">
                          {/* <DatePickerComponent2></DatePickerComponent2> */}
                          <span className="text-[11px]">{getTrackTitle(attempt.track_entry_id)}</span>
                         {showIds && <span className="text-[11px]">{` (${attempt.track_entry_id})`}</span>}

                          <DatePickerComponent label={"Date:"} value={attempt.date} style={""}
                           path={{ "_id": attempt._id, "path": "date", "index": null, "field": null, "collection": "upload_attempts" }}>
                          </DatePickerComponent>

                          <EditableText label={"Error:"} value={attempt.error} style={""}
                           path={{ "_id": attempt._id, "path": "error", "index": null, "field": null, "collection": "upload_attempts" }}> </EditableText>
                        </div>
                        <div onClick={()=> eel.delete_entry({ "_id": attempt._id, "collection": "upload_attempts" } )} 
                         className=" cursor-pointer bg-red-500 w-[7px] rounded-r-xl ml-2"></div>

                      </div>
                      // <AttemptUploadComponent key={`${i}`} attempt={attempt}></AttemptUploadComponent>
                    ) : <div key={`${i}_platform`}></div> )}
                  </div>
                {/* </ul> */}
              </div>
              : <div key={`${platform}_${_id}`} ></div>
          ))}
        </ul>
        </div>
      }
      <div className={` _h-[200px] flex items-center _justify-center ${attemptShow != "None" ? "mt-3":" _border-l px-3 border-[#707070]" } text-[12px]`}>
        <div className="bordered _mx-5 px-3">Id: {_id}</div>
        <button onClick={()=> eel.delete_entry({ "_id": _id,"collection": "upload_sessions"} ) } className="mx-5 px-3 border border-[#707070] rounded-xl">Delete track entry</button>
      </div>
      
    </div>
  );

  function getTrackTitle(track_entry_id) {
    const ret = compRef.state.track_entries.find(item => item._id === track_entry_id)
    return ret ? ret.track_title : "track not found";
  }

  function platformElem(platform) {
    return <div className=" text-center"> {platform}:
      <div
         onClick={() =>{ if (!compRef.state.track_entries.length || getTrackTitle(selectedTrack) == "track not found") alert("No track entries"); 
         else eel.create_entry({ "track_entry_id": selectedTrack, "session_entry_id": _id, "site": platform, "date": new Date(), "error":"", "collection": "upload_attempts" })}} 
        // onClick={() => eel.add_field({ "_id": _id, "path": `uploads.${platform}.upload_attempts`, "field": null, "value": {"site": platform, "date": "", "error": "" } })}
        
        className="inline ml-1 border border-[#909090] rounded-xl px-1 _h-[20px] cursor-pointer">+</div>
    </div>;
  }
};

export default UploadSessionComponent;
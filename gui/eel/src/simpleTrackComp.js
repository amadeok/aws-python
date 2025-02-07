
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
import { formatDate, getFileNameFromPath } from "./utils";
import BarsChart from "./BarsInfoCharComp";

const SimpleTrackComponent = ({ track, ctx, isLast }) => {

  const { } = useContext(AppContext);
  // console.log("theme", attemptShow)
  const { _id, track_title, op_number, grade, for_distrokid, upload_attempts, entry_status, file_details, insertion_date, secondary_text } = track;
  const { attemptShow, showIds, selectedTrack, selectedSession, HL, setHL } = ctx
  const [showBarsChar, setShowBarsChar] = useState(false)


  useEffect(() => {
  }, [])

  useEffect(() => {
    // console.log("------------------->", upload_attempts, upload_attempts.filter(obj => obj.site === "threads"))
  }, [track])

  const { upload_sites } = compRef.state
  const isInArray = (string, array) => array.includes(string);
  const getPathBase = (path, field = null) => { return { "_id": _id, "path": path, "index": null, "field": field, "collection": "track_entries" } }

  const platformN = upload_sites.length
  const platformPerc = 100 / platformN
  let Styles = "  text-left   py-0 border-[#707070] items-center _h-fit pl-1 "
  // _grow _w-[20%] _flex-[10%] _w-[10%]
  let borderStyles = isLast ? "border border-r-0" : "border border-r-0 border-b-0"
  // let SpanStyle = 
  Styles += borderStyles
  return (
    <div className="text-[#bebebe] text-center">
      <div className="grid grid-cols-12 _flex ">
        {/* <h2 className="_my-3 p-1 ">Track Details: </h2> */}
        {/* { isLast? " last" : "not last"  } */}
        {showBarsChar && <BarsChart _id={_id} isOpen={showBarsChar} setIsOpen={setShowBarsChar} file_details={file_details} ></BarsChart>}

        <EditableText label={""} value={track_title} style={"text-left flex  col-span-3  border-[#707070] items-center pl-1 " + borderStyles} path={getPathBase("track_title")}> </EditableText>
        <EditableText label={""} value={op_number} style={Styles} path={getPathBase("op_number")} isNumber={true}> </EditableText>

        <EditableText label={""} value={grade} style={Styles} path={getPathBase("grade")}>  </EditableText>
        <CheckboxComponent label={""} value={for_distrokid} style={Styles} path={getPathBase("for_distrokid")}></CheckboxComponent>

        {/* <button onClick={()=>    eel.open_file_select_window(_id)((ret)=> console.log(ret))} className={`${Styles}`}  onMouseEnter={()=>setHL(file_details.file_path)} onMouseLeave={()=> setHL(null)}>File: {getFileNameFromPath(file_details.file_path)} ({file_details.has_midi_file ? "Midi" : "No midi"}) </button> */}
        {/* <button className="flex flex-1 border border-[#707070] rounded-xl px-1 items-center text-[14px]" onClick={()=>setShowBarsChar(!showBarsChar )} >
          Bpm: {file_details.bpm} &nbsp; Bars: {file_details.bars} &nbsp; B/T: {file_details.bars_per_template} &nbsp;  B/B: {file_details.beats_per_bar}  </button> */}
        {/* <EditableText label={"Custom video:"} value={getFileNameFromPath(file_details.custom_video) || "disabled"} style={Styles} path={{ "_id": _id, "path": "file_details", "index": null, "field": "custom_video", "collection": "track_entries" }}>  </EditableText> */}
        {/* <div><button onClick={()=>    eel.open_file_select_window_custom_video(_id)((ret)=> console.log(ret))} className={`${Styles}`}  onMouseEnter={()=>setHL(file_details.file_path)} onMouseLeave={()=> setHL(null)}>File: {getFileNameFromPath(file_details.file_path)} </button></div> */}

        {/* <EditableText label={"Sec. text:"} value={secondary_text || "disabled"} style={Styles} path={getPathBase("secondary_text")}>  </EditableText> */}

        <DatePickerComponent label={""} value={insertion_date} style={Styles + " col-span-2"} path={getPathBase("insertion_date")}>   </DatePickerComponent>

        <EditableText label={""} value={entry_status} style={`${Styles}  outline  font-semibold ${entry_status == "ready" ? " text-[#ffffff]  bg-green-800 outline-1  outline-[#00ff00] " : " text-[#000000] bg-yellow-200  outline-[#ff0000] "}`}
          path={getPathBase("entry_status")} validator={(text) => { console.log("validator", text); const arr = ["ready", "pending", "error"]; return (text != "ready" || file_details.drive_id.length) && isInArray(text, arr) ? null : `${text} not in ${arr} or no file uploaded` }}> </EditableText>
        <div className=" cursor-pointer" onClick={() => console.log("playing track" + op_number) || eel.play_track({track_n: op_number})} >{`P.`}{`${op_number}`} </div>
        <div className={Styles}>
          {/* "flex flex-1  justify-start mt-2 text-[12px]"> */} 
          <button onClick={() => eel.delete_entry({ "_id": _id, "collection": "track_entries" })} className="_mx-5 _px-3 _border _rounded-xl ">Delete</button>
        </div>

        <div className={Styles}>{_id}</div>

      </div>
      {(attemptShow !== "None" && true) &&
        <div className="mt-3 border rounded-xl border-[#707070] p-2">
          <h3>Uploads</h3>
          <ul className="_grid _grid-flow-col _auto-cols-max flex justify-start flex-wrap">
            {upload_sites.map((platform, i) => (
              // uploads[platform].upload_attempts.length || 1
              true ?
                <div key={`${platform}_${_id}_${i}`} className={` ${i < platformN - 1 ? "border-r" : ""} w-[50%] md:w-[14.28%] _flex-[0.1] px-2 border-[#707070] `}>
                  {/* <ul > */}
                  <div className="flex flex-col  _bg-red-200  _w-[30%]">
                    {platformElem(platform)}

                    {upload_attempts && upload_attempts.filter(obj => obj.site === platform).map((attempt, i) => attempt.error.length || attemptShow === "All" ?
                      (
                        <div key={`${i}_platform`} className={`flex text-[#bebebe] text-left pl-2 _px-2 _py-1 my-[2px] border ${attempt.error.length ? "border-[#ff0000] _border-[5px]" : "border-[#707070]"}  rounded-xl justify-between`}>
                          <div className="_grow">
                            <div className="flex items-center">
                              <div className="grow">
                                <DatePickerComponent label={"Date:"} value={attempt.date} style={null}
                                  path={{ "_id": attempt._id, "path": "date", "index": null, "field": null, "collection": "upload_attempts" }}>  </DatePickerComponent>
                              </div>
                              <div className="pl-[3px] w-[13px] text-[12px]">
                                ({getSessionDate(attempt.session_entry_id, true)})
                              </div>
                            </div>
                            <div onMouseEnter={() => setHL(attempt.error)} onMouseLeave={() => setHL(null)}>
                              <EditableText label={"Error:"} value={attempt.error} style={"max-h-[70px] overflow-hidden"} path={{ "_id": attempt._id, "path": "error", "index": null, "field": null, "collection": "upload_attempts" }}> </EditableText></div>
                          </div>
                          <div onClick={() => eel.delete_entry({ "_id": attempt._id, "collection": "upload_attempts" })}
                            className=" cursor-pointer bg-red-500 max-w-5 rounded-r-xl ml-1 pl-1"></div>

                        </div>
                        //  <div key={`${i}_platform`}>

                        //   </div>

                      )
                      : <div key={`${i}_platform`}></div>)}
                  </div>
                  {/* </ul> */}
                </div>
                : <div key={`${platform}_${_id}`} ></div>
            ))}
          </ul>
        </div>
      }


    </div>
  );

  function getSessionDate(session_entry_id, getIndex = false) {
    const ret = getIndex ? compRef.state.upload_sessions.findIndex((item) => item._id === session_entry_id) : compRef.state.upload_sessions.find((item) => item._id === session_entry_id)
    return ret != null ? (getIndex ? ret : formatDate(new Date(ret.date))) : "session not found";
  }

  function platformElem(platform) {
    return <div className=" text-center"> {platform}:
      <div
        onClick={() => {
          if (!compRef.state.upload_sessions.length || getSessionDate(selectedSession) == "session not found") alert("No upload session "); else
            eel.create_entry({ "track_entry_id": _id, "session_entry_id": selectedSession, "site": platform, "date": new Date(), "error": "", "collection": "upload_attempts" })
        }}
        // onClick={() => eel.add_field({ "_id": _id, "path": `uploads.${platform}.upload_attempts`, "field": null, "value": {"site": platform, "date": "", "error": "" } })}

        className="inline ml-1 border border-[#909090] rounded-xl px-1 _h-[20px] cursor-pointer">+</div>
    </div>;
  }
};

export default SimpleTrackComponent;
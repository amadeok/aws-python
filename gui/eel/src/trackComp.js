
import { useState, useEffect } from "react";
import EditableText from "./EditableText";
import CheckboxComponent from "./CheckboxComponent";
//import uploadAttempComponent from "./uploadAttempComp";
// import TrackComponent2 from "./attempComp";
import AttemptUploadComponent from "./AttemptUploadComponent";
import { compRef } from "./App";
import { eel } from "./eel";
import { AppContext } from './AppContext';
import { useContext } from "react";

const TrackComponent = ({ track }) => {

  const { attemptShow, setAttemptShow } = useContext(AppContext);
  console.log("theme", attemptShow)
  const { _id, track_title, grade, for_distrokid, uploads } = track;
  // useEffect(() => {
  //     console.log("------------------->", track)
  // }, [track])

  // Object.keys(uploads).map((platform) => (
  //   console.log("----------->", uploads, uploads[platform].upload_attempts)
  // ))

  function setter(t) {
    // compRef.setState({"track_title": t})
    track.track_title = t
    console.log("------------------->setter", track.track_title, track)
  }
  const platformN = Object.keys(uploads).length
  const platformPerc = 100/platformN
  const Styles = "_grow _w-[20%] flex-1 text-left border rounded-xl mx-2 p-2 py-1 border-[#707070] "

  return (
    <div className="text-[#bebebe]">
      <div className="flex _grow   justify-evenly">
        <h2 className="_my-3 p-1 ">Track Details: </h2>
        {/* <EditableText initialValue={"test"} ></EditableText> */}
        <EditableText label={"Track Title:"} value={track_title} style={Styles}
          path={{ "_id": _id, "path": "track_title", "index": null, "field": null }}>
        </EditableText>
        <EditableText label={"Grade:"} value={grade} style={Styles}
          path={{ "_id": _id, "path": "grade", "index": null, "field": null }}>
        </EditableText>
        <CheckboxComponent label={"For DistroKid:"} value={for_distrokid} style={Styles}
          path={{ "_id": _id, "path": "for_distrokid", "index": null, "field": null }}
        ></CheckboxComponent>
        {/* <p className={Styles}  >For DistroKid: {for_distrokid.toString()}</p> */}

      </div>
      { attemptShow !== "None"  &&
      <div className="my-3 border rounded-xl border-[#707070] p-2">
        <h3>Uploads</h3>
        {/* Rendering upload details for each platform */}
        <ul className="_grid _grid-flow-col _auto-cols-max flex justify-start flex-wrap">
          {Object.keys(uploads).map((platform, i) => (
            uploads[platform].upload_attempts.length || 1 ?
              <div key={`${platform}_${_id}_${i}`} className={` ${i < platformN - 1 ? "border-r" : ""} w-[50%] md:w-[14.28%] _flex-[0.1] px-2 border-[#707070] `}>
                {/* <ul > */}
                  <div className="flex flex-col  _bg-red-200  _w-[30%]">
                    {platformElem(platform)} 
                  
                    {true &&uploads[platform].upload_attempts.map((attempt, i) => attempt.error.length ||  attemptShow === "All" ? (
                      <div key={i} className="flex text-[#bebebe] text-left pl-2 _px-2 _py-1 my-[2px] border border-[#707070] rounded-xl justify-between">
                        <div  className="_grow">
                          <EditableText label={"Date:"} value={attempt.date} style={""}
                            path={{ "_id": _id, "path": `uploads.${platform}.upload_attempts`, "index": i, "field": "date" }}>
                          </EditableText>
                          <EditableText label={"Error:"} value={attempt.error} style={""}
                            path={{ "_id": _id, "path": `uploads.${platform}.upload_attempts`, "index": i, "field": "error" }}>
                          </EditableText>
                        </div>
                        <div onClick={()=> eel.delete_field({ "_id": _id, "path": `uploads.${platform}.upload_attempts`, "field": null,"index": i } )} 
                         className=" cursor-pointer bg-red-500 w-2 rounded-r-xl ml-2"></div>

                      </div>
                      // <AttemptUploadComponent key={`${i}`} attempt={attempt}></AttemptUploadComponent>
                    ) : <div></div> )}
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

  function platformElem(platform) {
    return <div className=" text-center"> {platform}:
      <div
        onClick={() => eel.add_field({ "_id": _id, "path": `uploads.${platform}.upload_attempts`, "field": null, "value": { "date": "", "error": "" } })}
        className="inline ml-1 border border-[#909090] rounded-xl px-1 _h-[20px] cursor-pointer">+</div>
    </div>;
  }
};

export default TrackComponent;
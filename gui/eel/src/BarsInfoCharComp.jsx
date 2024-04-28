import React, { useEffect, useState } from 'react';
import './App.css';
import DynamicWidthElements from './DynElems';
import { eel } from './eel';

function BarsChart({_id, isOpen, setIsOpen, file_details}) {

  // console.log("fffffff", file_details)
  const [bpm, setBpm] = useState(file_details.bpm);
  const [bars, setBars] = useState(file_details.bars);
  const [barsPerTemplate, setBarsPerTemplate] = useState(file_details.bars_per_template);
  const [beatsPerBar, setBeatsPerBar] = useState(file_details.beats_per_bar);
  const [customDursObj, setCustomDursObj] = useState(file_details.avee_custom_lenghts);
  const [customDurs, setCustomDurs] = useState(Array.from({ length: 0 }, (_, i) => 2.1));
  const [barPositions, setBarPositions] = useState([]);
  const [initCustomDurs, setInitCustomDurs] = useState(Array.from({ length: 200 }, (_, i) => bpmToSeconds(file_details.bpm)*file_details.beats_per_bar*file_details.bars_per_template));

  const [elements, setElements] = useState([ ]);

  useEffect(() => {
      console.log("-------> init", initCustomDurs)
  
    return () => {    }
  }, [])
  

  const getPath = (path, field=null) => {return { "_id": _id, "path": path, "index": null, "field": field, "collection": "track_entries" }}

    const addElement = (w) => {
      const newElement = {
        id: elements.length + 1,
        minWidth: "2000px",
        width: `${w}%`,
        backgroundColor: 'gray' // Example default background color for new elements
      };
      // setElements(prevElements => [...prevElements, newElement]);
      return newElement
    };

  // useEffect(() => {
  //    console.log("----->", customDurs, barPositions, (customDurs[0] / bars)*100)
  //    setbarPositions(      customDurs.map((elem, i) => (customDurs[i] /bars)*100  ) )
  //   return () => {   }
  // }, [customDurs, bars])

  useEffect(() => {
    console.log("----- barPositions >", barPositions)
  }, [barPositions])
  
  useEffect(() => {
    console.log("----- bars >", bars)
    //  console.log("----->", customDurs, barPositions, (customDurs[0] / bars)*100)
     const arr =  customDurs// Array.from({ length: 200 }, (_, i) => bpmToSeconds(bpm)*beatsPerBar*barsPerTemplate);
    //  const keys = Object.keys(customDursObj);
    //  for (let i = 0; i < keys.length; i++) {
       
    //    const index = Number(keys[i])
    //    const dur =  customDursObj[index]
    //    arr[index] = dur.dur
    //    console.log("--->", index,dur);
    //  }
     let arr2 = []
     let pos = 0
     for (var i =0; i < bars+1; i++){
      arr2.push(pos)
      pos+=arr[i]
     }
     setBarPositions(arr2)
  }, [customDurs])


  useEffect(() => {
    console.log("----- customDursObj >", customDursObj)

    const arr =  Array.from({ length: 200 }, (_, i) => bpmToSeconds(bpm)*beatsPerBar);
    const keys = Object.keys(customDursObj);
    for (let i = 0; i < keys.length; i++) {
      
      const index = Number(keys[i])
      const dur =  customDursObj[index]
      arr[index] = dur.dur
      console.log("--->", index,dur);
    }

    setCustomDurs(      arr.slice(0, bars) ) 


  }, [customDursObj, bars, bpm, beatsPerBar])
  

  useEffect(() => {
    console.log("----- customDurs >", customDurs)
    const elems = customDurs.map((elem, i) => addElement((customDurs[i] /bars)*100  )  )
    setElements(elems);
  }, [customDurs])

  useEffect(() => {   
    console.log("----- customDursObj >", customDursObj)
  }, [customDursObj])
  
  
  useEffect(() => {
    console.log("----- elements >", elements)
  }, [elements])
  const handleBpmChange = (event) => {
    setBpm(event.target.value);
  };
  const handleBarsChange = (event) => {
    setBars(event.target.value);
  };
  const handleBarsPerTemplateChange = (event) => {
    setBarsPerTemplate(event.target.value);
  };
  const handleBeatsPerBarChange = (event) => {
    setBeatsPerBar(event.target.value);
  };

  const handleCustomDurChange = (event, i) => {
    console.log("handle dur change",  i,  " | ",customDursObj, " | ", event && event.target.value)
    let obj = _.cloneDeep(customDursObj)
    if (event)
      obj[i] = {"dur": Number(event.target.value)}
    else 
      delete obj[i]
     setCustomDursObj(obj)
  }

  const handleSubmit = () => {
    eel.update_field({ ...getPath("file_details", "bpm"), value: Number(bpm) });
    eel.update_field({ ...getPath("file_details", "bars"), value: Number(bars) });
    eel.update_field({ ...getPath("file_details", "bars_per_template"), value: Number(barsPerTemplate) });  
    eel.update_field({ ...getPath("file_details", "beats_per_bar"), value: Number(beatsPerBar) });  
    eel.update_field({ ...getPath("file_details", "avee_custom_lenghts"), value: customDursObj});   

  }
  function generateRange(maxNumber) {
    return Array.from({ length: maxNumber }, (_, i) => i + 1);
  }
  const numbers = generateRange(bars);
  function bpmToSeconds(bpm) {    return 60 / bpm;}
   const btStyle = "p-2 mx-1 py-1 rounded-xl border bg-[#444] text-white"
  return (
    <div className="text-black  absolute w-full flex justify-center">
      {/* <div className='bg-red-200'> .................!{file_details.bpm}!....</div> */}
      <div className='absolute top-[50vh] translate-y-[-50%] bg-[#444] p-5 rounded-xl border w-[90%]  '>
      <h2 className='text-white'>Modify Parameters</h2>

        <div className="grid grid-rows-4 grid-flow-row gap-4 justify-center  place-items-start content-end popup_bpm ">
        <div className="">  <label >BPM:</label>
          <input type="number" value={bpm} onChange={handleBpmChange} />
        </div>
        <div>   <label>Bars:</label>
          <input type="number" value={bars} onChange={handleBarsChange} />
        </div>
        <div>    <label>Bars Per Template:</label>
          <input type="number" value={barsPerTemplate} onChange={handleBarsPerTemplateChange} />
        </div>
        <div>  <label>Beats Per Bar:</label>
          <input type="number" value={beatsPerBar} onChange={handleBeatsPerBarChange} />
        </div>
        </div>
        <div className='flex w-full items-center justify-center mt-4 '>
        <button className={btStyle} onClick={handleSubmit}> Submit </button>
        <button className={btStyle} onClick={()=> setIsOpen(false)}>   Cancel </button>
        </div>
        <div className='flex mx-5 mt-5'>
        {elements.map((element, i) => (
          <div className={`${(i+1) % barsPerTemplate == 0 ? "border-r-4 border-r-[#ff0000]" : " border-l "} border-2 ${i != 0 && "border-l-0"} border-[#303030] _overflow-hidden text-left`}
            key={i}
            style={{
              width: element.width,
              height: "50px",
              backgroundColor: element.backgroundColor,
              // border: "1px",
              borderStyle: "solid"
            }}
          >
            {/* <div> */}
              <input
              className='_h-full w-full bg-[#666]'
                type="number"
                value={Math.floor(customDurs[i] * 1000) / 1000}
                onChange={(event)=> handleCustomDurChange(event, i)}
                placeholder={Math.floor(customDurs[i] * 1000) / 1000}
              />
              <div>
              <p className=' cursor-pointer' onClick={(event)=> handleCustomDurChange(null, i)}>{Math.floor(barPositions[i] * 1000) / 1000}s</p>
              {/* <div className='h-[7px] z-50 bg-yellow-400 w-full'></div> */}
              </div>
            {/* </div> */}
          {/* <div className='ml-1'> {Math.floor(barPositions[i] * 1000) / 1000}s</div> */}
          {/* i*(bpmToSeconds(bpm)*beatsPerBar) */}
          </div>
        ))}
        </div>

        {/* <DynamicWidthElements></DynamicWidthElements> */}
        {/* <div className='flex just' >
          {numbers.map((number, i) =>
            <div style={{width: ` ${barPositions[i]}%`}} className={`outline _w-[13.4%] inline    outline-1`} key={number.toString()}>
              {number}
            </div>
          )}
        </div> */}
        {/* <div style={{ height: '300px', width: '600px' }}>
        <Line data={data} />
      </div> */}
      </div>
    </div>
  );
}

export default BarsChart;

import React, { useState, useEffect } from 'react';
import { eel } from "./eel.js";

function EditableText({ label, value, style, path, validator = null, isNumber=false }) {
  const [isEditing, setIsEditing] = useState(0);
  const [text, setText] = useState(value);
  const [lastGoodtext, setLastGoodtext] = useState(value);

  useEffect(() => {
    if (value)
      setText(value)
    return () => { }
  }, [value])


  const handleDoubleClick = () => {
    console.log("----> double click")
    setIsEditing(true);
  };

  function getn(val) {
    return isNumber ? Number(val) : val;
  }
  const handleChange = (e) => {
    setText( e.target.value);
  };

  function submit() {
    setIsEditing(false);

    if (validator) {
      const ret = validator(text);
      if (ret) {
        alert("validator fail:  " + ret);
        setText(lastGoodtext);
      }
      else {
        setLastGoodtext(text);
        eel.update_field({ ...path, value: getn(text) });
      }
    } else
      eel.update_field({ ...path, value: getn(text) });

  }

  const handleKeyPress = (event) => {
    if (event.key === 'Enter') {
      console.log('Enter key pressed! Value:', event.key);
      submit();
    }
  };

  const handleBlur = () => {
    submit();
    //  setIsEditing(false);
    //  eel.update_field({...path, value: text})
  };
  const max = 40
  return (
    <div className={`${style} flex ${text && text.length > max ? "flex-col" : ""}`}>
      <div className='grow-[0] _w-[100px] '>    {label}    </div>
      {isEditing ? (
        <input
          className='ml-2 inline _grow _shrink-[2] _min-w-0 _w-0 bg-[#303030] '
          type={isNumber? "number" : "text"}
          value={text}
          onChange={handleChange}
          onBlur={handleBlur}
          onKeyDown={handleKeyPress}
          autoFocus
        />
      ) : (
        <div className={` _text-wrap break-all min-w-[30%] _inline  _whitespace-normal _overflow-hidden  _bg-slate-500 ${text && text.length > max ? "" : "pl-2"}`} onClick={handleDoubleClick}>{text}</div>
      )}
    </div>
  );
}

export default EditableText;
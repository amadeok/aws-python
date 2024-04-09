import React, { useState } from 'react';
import { eel } from "./eel.js";

function CheckboxComponent({value, label, style, path}) {
  const [isChecked, setIsChecked] = useState(value);

  const handleCheckboxChange = (event) => {
    setIsChecked(event.target.checked);
    console.log("event.target.checked", event.target.checked)
    if (path)
      eel.update_field({ ...path, value: event.target.checked })

  };

  return (
    <div className={style}>
      <label>
        <span className='pr-2'>
      {label}
      </span>
        <input
          type="checkbox"
          checked={isChecked}
          onChange={handleCheckboxChange}
        />
      </label>
    </div>
  );
}

export default CheckboxComponent;

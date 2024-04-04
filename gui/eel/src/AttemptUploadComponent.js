import React from 'react'

const AttemptUploadComponent = ({ attempt }) => {
    const { date, error } = attempt;
    // console.log("attempt", attempt)
    return (
        <div className="text-[#bebebe] text-left px-1 border border-[#707070] rounded-xl">
            <p>date: {date}</p>
            <p>error: {error}</p>

        </div>
    );
}

export default AttemptUploadComponent
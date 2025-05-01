function generateExtraElems(count) {
    const extraElems = [];

    for (let i = 1; i <= count; i++) {
        extraElems.push({
            [`i${i}`]: {
                "left_click": (data, cell) => {
                    console.log(`playing iteration ${i}`, data, cell);
                    const audio = document.getElementById("audio-element");
                    const opNumber = data["op_number"];
                    audio.src = `/get_audio?op=${opNumber}&it=${i}`;
                    audio.play();
                },
                "right_click": async (data, cell) => {
                    console.log(`opening folder op: ${data["op_number"]} it: ${i}`, data, cell);
                    await fetch(`/open_folder?op=${data["op_number"]}&it=${i}`, {
                        method: 'GET',
                    })
                },
                "colWeight": 0.1,
                "inputType": "button"
            }
        });
    }
    const delElem = {
        "D": {
            "colWeight": 0.1,
            "inputType": "button",
            "left_click": (data, cell) => {
                console.log("DEL", data)
                if (confirm(`Are you sure you want to delete op. ${data["op_number"]}?`)) {
                    // User clicked OK
                    console.log("Item will be deleted");
                    fetch(`/delete_entry?_id=${data["_id"]}&collection=track_entries`, {
                        method: 'GET',
                    })
                        .then(response => {
                            if (!response.ok) { throw new Error('Network response was not ok'); }
                            return response.json(); // or response.text() if the server doesn't send JSON
                        })
                        .then(data => { console.log('Success:', data); document.redrawAll() })
                        .catch(error => { console.error('Error:', error); });
                }
                else {
                    // User clicked Cancel
                    console.log("Deletion canceled");
                }
                // http://localhost:3000/delete_entry?_id=6812d468abe02cc54f26dde7&collection=track_entries
            },
            "right_click": async (data, cell) => {
                console.log(`opening folder ${data["op_number"]}`, data, cell);
                await fetch(`/open_folder?op=${data["op_number"]}`, {
                    method: 'GET',
                })
            },
        }
    }
    extraElems.push(delElem)
    return extraElems;
}

export const config =
{
    "insertion_date": {
        // "parseFunc": (data, cell) => {
        //     const date = new Date(data);
        //     return date.toLocaleString()
        // },
        "colWeight": 1,
        "inputType": "datetime-local",
        "jsCallback": (data) => {
            console.log("--->jsCallback", data)
        },
        "pythonCallback": "test"
    },
    "file_details": {
        "parseFunc":
            (data, cell) => {
                // console.log("file_details", cell);
                cell.style.backgroundColor = 'lightblue'; // or use 'color' for text color
                // cell.style.padding = '0px 10px';
                // cell.textContent = 'Your text here'; // or innerHTML if you need HTML content
                return data + "!"
            },
        "colWeight": 4
    },
    "for_distrokid": {
        "colWeight": 2
    },
    "op_number": {
        "inputType": "number",
        "colWeight": 0.5,
    },
    "for_distrokid": {
        "inputType": "checkbox",
        "colWeight": 1
    },
    "grade": {
        "colWeight": 0.1
    },
    "order": ["track_title", "op_number", "grade", "entry_status", "for_distrokid", "insertion_date"],
    //"order": [ "for_distrokid"],
    "title": "Tracks",

    "DOMContentLoaded": () => {
        const cont = document.getElementById("title-container")
        Object.assign(cont.style, {
            display: 'flex',
            flexDirection: 'row',
            alignItems: 'center',
            justifyContent: 'flex-start',
            margin: "10px 10px",
            // height: '200px',
            //border: '1px solid #ccc'
        });

        const audio = new Audio();
        audio.id = "audio-element"
        audio.controls = true;
        Object.assign(audio.style, { height: '30px', paddingLeft: "20px" });
        cont.appendChild(audio);

        const newBtn = document.createElement('button');
        newBtn.inputType = "button"
        newBtn.className = "btn"
        newBtn.textContent = "New"
        Object.assign(newBtn.style, {
            // height: '20px', 
            marginLeft: "10px",
            width: "50px",
            padding: "5px"
        });
        newBtn.addEventListener("click", async (e) => {
            console.log("e", e)
            await fetch("/create_entry").then(() => document.redrawAll())
        })
        cont.appendChild(newBtn);

        // let failedAttempts = 0; // Track failed requests
        // const interval = setInterval(() => 
        // fetch('/health')
        //     .then(() => failedAttempts = 0) // Reset on success
        //     .catch(() => ++failedAttempts > 0 && // Increment and check
        //     (clearInterval(interval), window.close())), // Close after 3 failures
        // 1000); // Check every second


    },

    "extraElems": generateExtraElems(3)
}

export const config =
{
    "insertion_date": {
        "parseFunc": (data, cell) => {
            const date = new Date(data);
            return date.toLocaleString()
        },
        "colWeight": 3
    },
    "file_details": {
        "parseFunc":
            (data, cell) => {
                // console.log("file_details", cell);
                cell.style.backgroundColor = 'lightblue'; // or use 'color' for text color
                // cell.style.padding = '0px 10px';
                // cell.textContent = 'Your text here'; // or innerHTML if you need HTML content
                return  data+ "!"
            },
            "colWeight": 4
    }
}

export const order =
{
    "order": []
}

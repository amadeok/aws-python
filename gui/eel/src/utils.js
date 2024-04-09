export function updateNestedField(obj, path, index, field, value) {
    const keys = path.split('.');
    let current = obj;

    for (let i = 0; i < keys.length - 1; i++) {
        const key = keys[i];
        if (!current[key]) {
            current[key] = {};
        }
        current = current[key];
    }

    const lastKey = keys[keys.length - 1];

    if (field === null || field === undefined) {
        if (index === null || index === undefined) {
            current[lastKey] = value;
        } else {
            if (!Array.isArray(current[lastKey])) {
                throw new Error('The specified path does not point to an array.');
            }
            current[lastKey][index] = value;
        }
    }
    else {
        if (index === null || index === undefined) {
            current[lastKey][field] = value;
        } else {
            if (!Array.isArray(current[lastKey])) {
                throw new Error('The specified path does not point to an array.');
            }
            current[lastKey][index][field] = value;
        }
    }
}
function padz(n, places = 2) {
    return String(n).padStart(places, '0');
  }

export function formatDate(date) {
    let formattedDate = `${date.getDate()}-${date.getMonth() + 1}-${date.getFullYear()}`;
    formattedDate += ` ${padz(date.getHours())}:${padz(date.getMinutes())}`;

    return formattedDate
  }

// let obj = {
//     a: {
//         b: {
//             c: [
//                 { id: 1, name: "Alice" },
//                 { id: 2, name: "Bob" },
//                 { id: 3, name: "Charlie" }
//             ],
//             d : [
//                 "car", "shift", "boat"
//             ]
//         },
//         e: "crack"
//     }
// };

// updateNestedField(obj, 'a.b.c', 1, 'name', 'Updated Bob');
// updateNestedField(obj, 'a.b.d', 2, null, 'Updated boat');
// updateNestedField(obj, 'a.e', null, null, 'Updated crack');
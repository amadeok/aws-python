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

  export function getFileNameFromPath(filePath) {
    // Split the file path by the directory separator
    var parts = filePath.split(/[\\/]/);
    // Retrieve the last part which will be the file name
    var fileName = parts.pop();
    // If you want to handle cases where the filename has query params, remove them
    fileName = fileName.split('?')[0];
    return fileName;
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

export const lorem_ipsum = "sit nulla duis esse cillum Lorem nisi sunt fugiat nisi ex pariatur esse excepteur nostrud dolore sit officia mollit pariatur labore in eiusmod in eiusmod velit adipisicing esse quis nostrud id dolore velit ad est proident magna aliqua ut irure irure nisi qui sint do ut exercitation elit esse ex ex aliqua minim velit quis veniam aliqua ex in ullamco do labore non voluptate cupidatat labore dolore cupidatat commodo qui ex qui pariatur ad fugiat in consequat aliquip aliquip anim et et laborum sunt ea esse veniam excepteur enim elit sint esse ipsum ullamco duis nostrud ullamco sunt id consectetur anim veniam anim velit eu eu cupidatat magna do aute amet officia excepteur quis esse anim exercitation nisi dolor fugiat consectetur labore ipsum velit sit consectetur excepteur est non ullamco et eiusmod ut commodo occaecat sunt cillum ipsum veniam aute incididunt enim sint fugiat est non ullamco sit sunt minim dolore labore nulla sunt qui occaecat anim adipisicing eiusmod ullamco sunt enim mollit qui magna amet nostrud irure adipisicing deserunt do officia fugiat incididunt id eiusmod ipsum excepteur laborum ullamco ullamco cupidatat amet cupidatat adipisicing amet cillum quis elit in pariatur excepteur labore dolor elit cupidatat reprehenderit pariatur qui nisi"
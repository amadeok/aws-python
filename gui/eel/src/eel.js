export const eel = window["eel"];

// eel.expose(sayHelloJS);
// function sayHelloJS(x) {
//   console.log(x);
// }
//window.eel.expose( sayHelloJS, 'say_hello_js22' )


// eel.expose(getFiles);
// function getFiles(files)
// {
//   files.map((file) => {
//     document.querySelector(".para").innerHTML += String(file);
//   });
// }


function consolelog(x) {
  console.log(x);
}
window.eel.expose( consolelog, 'console_log' )



// 'use strict';

// const video = document.getElementById('video');
// const canvas = document.getElementById('canvas');
// const snap = document.getElementById("snap");
// const errorMsgElement = document.querySelector('span#errorMsg');

// const constraints = {
//     audio: true,
//     video: {
//         width: 1280, height: 720
//     }
// };

// // Access webcam
// async function init() {
//     try {
//         const stream = await navigator.mediaDevices.getUserMedia(constraints);
//         handleSuccess(stream);
//     } catch (e) {
//         errorMsgElement.innerHTML = `navigator.getUserMedia error:${e.toString()}`;
//     }
// }

// // Success
// function handleSuccess(stream) {
//     window.stream = stream;
//     video.srcObject = stream;
// }

// // Load init
// init();

// // Draw image
// var context = canvas.getContext('2d');
// snap.addEventListener("click", function () {
//     context.drawImage(video, 0, 0, 640, 480);
// });

// studentImage = document.getElementById('student_img');
// imgData = getBase64Image(studentImage);
// localStorage.getItem("imgData", imgData);

// studentImage.src = "data:image/png;base64," + dataImage;

// function getBase64Image(img) {
//     var canvas = document.createElement("canvas");
//     canvas.width = img.width;
//     canvas.height = img.height;

//     var ctx = canvas.getContext("2d");
//     ctx.drawImage(img, 0, 0);

//     var dataURL = canvas.toDataURL("image/png");

//     return dataURL.replace(/^data:image\/(png|jpg);base64,/, "");
// }
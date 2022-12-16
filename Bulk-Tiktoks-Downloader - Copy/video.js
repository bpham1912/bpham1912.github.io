const https = require("https");
const fs = require("fs");

const url2 = "https://www.tikwm.com/video/media/hdplay/7171785897724153114.mp4";
const url11 = "https://www.tikwm.com/video/media/hdplay/7171785897724153114.mp4"; 

//var ulrs_1= new Array;
const followRedirect = require('follow-redirect-url');

followRedirect.startFollowing(url2).then(urls => {
	
	console.log(Object.values(urls));

Object.values(urls).forEach(value => {
  //console.log(value.redirectUrl);
  const ulr_var = value.redirectUrl;
  console.log(ulr_var);
  // https.get(url2, function(res){
     // const fileStream = fs.createWriteStream("video.mp4");
     // res.pipe(fileStream);
    // fileStream.on("finish", function(){
         // fileStream.close();
        // console.log("Done!");
    // });
 // });
})
//const objectArray = Object.values(numbers);
//console.log(urls.redirectUrl);
	
}).catch(error => {
    console.log(error)
})
//var ulr_var = value.redirectUrl;


// URL of the image

  
// https.get(url,(res) => {

    // const path = `img.mp4`; 
    // const filePath = fs.createWriteStream(path);
    // res.pipe(filePath);
    // filePath.on('finish',() => {
        // filePath.close();
        // console.log('Download Completed'); 
    // })
// })




// function download(uri, filename) {
    // var protocol = url.parse(uri).protocol.slice(0, -1);
    // var deferred = Q.defer();
    // var onError = function (e) {
        // fs.unlink(filename);
        // deferred.reject(e);
    // }
    // require(protocol).get(uri, function(response) {
        // if (response.statusCode >= 200 && response.statusCode < 300) {
            // var fileStream = fs.createWriteStream(filename);
            // fileStream.on('error', onError);
            // fileStream.on('close', deferred.resolve);
            // response.pipe(fileStream);
        // } else if (response.headers.location) {
            // deferred.resolve(download(response.headers.location, filename));
        // } else {
            // deferred.reject(new Error(response.statusCode + ' ' + response.statusMessage));
        // }
    // }).on('error', onError);
    // return deferred.promise;
// };
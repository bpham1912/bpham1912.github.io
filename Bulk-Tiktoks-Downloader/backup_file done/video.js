const https = require("https");
const fs = require("fs");
const path = require("path");
const url2 = "https://www.tikwm.com/video/media/hdplay/7171785897724153114.mp4";
const url11 = "https://www.tikwm.com/video/media/hdplay/7171785897724153114.mp4"; 

//var ulrs_1= new Array;
const followRedirect = require('follow-redirect-url');

followRedirect.startFollowing(url2).then(urls => {
	
	console.log(Object.values(urls)); // xuất obj link từ URL gốc 2

Object.values(urls).forEach(value => {
  //console.log(value.redirectUrl);
  const ulr_var = value.redirectUrl; // lấy giá trị redirectUrl
  console.log(ulr_var); // xuất giá trị redirectUrl lên màn hình -> xuất được nhưng lỗi undefined
 const filename = path.basename(ulr_var); // xuất đường dẫn path, cần update -> ID video
//console.log(filename);
 //them
function downloadFile(ulr_var,callback){
	const req = https.get(ulr_var, function(res){
	const fileStream = fs.createWriteStream("./video.mp4"); // lưu video -> cần update tên video = ID video
	res.pipe(fileStream);
	
	fileStream.on("error",function(err){
		console.log("Lỗi k ghi file");
		console.log(err);
	});
	fileStream.on("close",function(){
		callback(filename);
	});
	fileStream.on("finish",function(){
		fileStream.close();
		console.log("Done! tải xong video");
	});
	
});

req.on("error",function(err){
	console.log("Lỗi tải FILE");
		console.log(err);
});

}

downloadFile(ulr_var,function(fn){
	console.log(fn);
});
 //end
 

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
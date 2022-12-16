const https = require("https");
const fs = require("fs");
const path = require("path");
const url2 = "https://www.tikwm.com/video/media/hdplay/7171785897724153114.mp4";
const url = "https://www.tikwm.com/video/media/hdplay/7171785897724153114.mp4"; 

const filename = path.basename(url);
//console.log(filename);
function downloadFile(url,callback){
	const req = https.get(url, function(res){
	const fileStream = fs.createWriteStream("video.mp4");
	res.pipe(fileStream);
	
	fileStream.on("error",function(err){
		console.log("Lỗi k ghi file");
		console.log(err);
	});
	fileStream.on("close",function(){
		callback(filename);
	});
	fileStream.on("finish",function()){
		fileStream.close();
		console.log("Done");
	});
	
});

req.on("error",function(err){
	console.log("Lỗi tải FILE");
		console.log(err);
});

}

downloadFile(url,function(fn){
	console.log(fn);
});
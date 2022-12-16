const vanillaPuppeteer = require('puppeteer');
const { addExtra } = require('puppeteer-extra');
const { pptr } = addExtra(vanillaPuppeteer);
const fetch = require('node-fetch');
const fs = require('fs');
const https = require('https');
const {Headers} = require('node-fetch');


//set a user-agent for fetch
const headers = new Headers();
headers.append('User-Agent', 'TikTok 26.2.0 rv:262018 (iPhone; iOS 14.4.2; en_US) Cronet');
headers.append('Content-Type', 'application/json');


main();
async function main() {
  //pptr.use(stealthPlugin())
  const browser = await pptr.launch( { headless: true ,args: ['--chrome.runtime','--navigator.languages','--iframe.contentWindow']} );
  const page = await browser.newPage();
    page.setUserAgent("Mozilla/5.0 (Macintosh; Intel Mac OS X 12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36");
  //delete browser profile after finish
  let chromeTmpDataDir = null;
  let chromeSpawnArgs = browser.process().spawnargs;
  for (let i = 0; i < chromeSpawnArgs.length; i++) {
      if (chromeSpawnArgs[i].indexOf("--user-data-dir=") === 0) {
          chromeTmpDataDir = chromeSpawnArgs[i].replace("--user-data-dir=", "");
      }
  }

  await page.evaluateOnNewDocument(() => {
    delete navigator.__proto__.webdriver;
  });
  //We stop images and stylesheet to save data
  await page.setRequestInterception(true);

  page.on('request', (request) => {
    if(['image', 'stylesheet', 'font'].includes(request.resourceType())) {
      request.abort();
    } else {
      request.continue();
    }
  })


  const args = process.argv.slice(2)
  const userLink = (args[0])
  if (userLink.includes("@")){
    console.log("Getting links from "+userLink)
  }else{
    console.log("Syntax error: \n\r use it like that: node bulktok https://www.tiktok.com/@profile")
    process.exit()
  }
  var nVideos = parseInt(args[1])



  await page.goto(userLink); //change this to user url page
  let username = page.url().slice(23,).replace(/[-:.\/*<>|?]/g,"");

  //scroll down until no more videos
  await autoScroll(page);

  //const urls = await page.evaluate(() => 
   // Array.from(document.querySelectorAll('div.tiktok-1qb12g8-DivThreeColumnContainer > div > div > div > div > div > a'), element => element.href));
 var urls = await page.evaluate(() => Array.from(document.querySelectorAll('div.tiktok-1qb12g8-DivThreeColumnContainer > div > div > div > div > div > a')).map((element) => element.href))
  //var videoDes = await page.evaluate(() =>Array.from(document.querySelectorAll('div.tiktok-1qb12g8-DivThreeColumnContainer.eegew6e2 > div > div > div > a')).map((items) => items.innerText))
    
    for (var i = urls.length; i--;) {
		
      urls[i] = urls[i] + '\n'}; //xuong dong
	  //let current_name = urls[i];
      fs.appendFile(username + '.txt' , urls + '', function (err) {
        if (err) throw err;
        console.log('Descriptions Saved!');
      });
      for (var i = urls.length; i--;) {
		  //let link = (urls[i]).slice(-19);
    let current_name = (urls[i]).slice(-19); // tên cho video.
	urls[i] = urls[i] + '\n'}; //xuong dong
	   fs.writeFile(username + '.txt' , urls + '', function (err))
	   {
		if (err) throw err;
        console.log('Da thay doi du lieu file');
	   }
	  }//end for
    if (args[1] == null || args[1] == NaN){
        var nVideos = String(urls.length);
      }

      browser.close();
      if (chromeTmpDataDir !== null) {
        fs.rm(chromeTmpDataDir, { recursive: true }, () => console.log('Deleted tmp profile'));
		
      }
	 

async function autoScroll(page){
  await page.evaluate(async () => {
      await new Promise((resolve, reject) => {
          var totalHeight = 0;
          var distance = 100;
          var timer = setInterval(() => {
              var scrollHeight = document.body.scrollHeight;
              window.scrollBy(0, distance);
              totalHeight += distance;

              if(totalHeight >= scrollHeight){
                  clearInterval(timer);
                  resolve();
              }
          }, 100);
      });
  });
}
function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}
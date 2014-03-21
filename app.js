//Import Dependencies
var http = require("http");
var url = require("url");
var querystring = require("querystring");
var fs = require("fs");
var exec = require("child_process").exec;
var formidable = require("formidable");

//Load HTML from disk
var radioPage = fs.readFileSync("html/radio.html");
var demodPage = fs.readFileSync("html/demod.html");

//This function gets called when we have an HTTP request
function onRequest(request, response) {
	var pathname = url.parse(request.url).pathname;
	console.log("Request for " + pathname + " received.");
	switch(pathname) {
		case '/':
			index(request, response);
			break;
		case '/radio':
			radio(request, response);
			break;
		case '/demod':
			demod(request, response);
			break;
		default:
			console.log("No request handler found for " + pathname);
			response.writeHead(404, {"Content-Type": "text/html"});
			response.write("404 Not found");
			response.end();
			break;
	}
}

//Start HTTP server
var server = http.createServer(onRequest).listen(8888);

function index(request, response) {
	//This is a temporary redirect to the GitHub info page
	response.writeHead(307, {"location": "http://zacinaction.github.io/kicksat/"});
	response.end();
}

function radio(request, response) {
	response.writeHead(200, {"Content-Type": "text/html"});
	response.write(radioPage);
	response.end();
}

function demod(request, response) {
	var form = new formidable.IncomingForm();
	form.keepExtensions = true;
	form.hash = 'sha1';
	form.uploadDir = "/tmp";
	form.parse(request, function(error, fields, files) {
		if(!files.upload)
		{
			//Redirect to the radio page if there is no form data
			response.writeHead(307, {"location": "/radio"});
			response.end();
		}
		else
		{
			response.writeHead(200, {"Content-Type": "text/html"});
			response.write(demodPage);

			var fileDir = "/home/zacman/RadioUploads/"+files.upload.hash;
			var filePath = fileDir+"/Recording.wav";
			fs.exists(filePath, function(exists) {
				if(!exists) {
					if(files.upload.path.substr(-4,4) == ".wav") {
						//Copy the .wav file and check it's validity with qwavheaderdump
						console.log(fields);
						exec("mkdir -p "+fileDir+" && cp "+files.upload.path+" "+filePath+" && "+"qwavheaderdump -F "+filePath, function(error, stdout, stderr) {

							var lines = stdout.split('\n');

							if(lines[1].trim() == "riff: 'RIFF'" && lines[3].trim() == "wave: 'WAVE'") {
								sampleRateLine = lines[8].trim();
								if(sampleRateLine == "sample rate: 192000" || sampleRateLine == "sample rate: 250000" || sampleRateLine == "sample rate: 256000") {
									//File is a valid .wav with correct sample rate
									response.write("<h1>Upload Successful!</h1> <h2>Your file looks good. We'll get to work demodulating it and email you the results. Thanks!</h2>");
									response.end("\n</div>\n</body>\n</html>");
								}
								else {
									//File is a valid .wav with bad sample rate
									response.write('<h1>Error:</h1> <h2>Sorry, this website is only set up to handle .wav files with sample rates of 192KHz, 250KHz, or 256KHz. <a href="https://groups.google.com/forum/#!forum/kicksat-gs">Contact us</a> if you need help.</h2>');
									response.end("\n</div>\n</body>\n</html>");
									exec("rm -R "+fileDir, function(error, stdout, stderr) {});
								}
							}
							else {
								//File is not a valid .wav
								response.write("<h1>Error:</h1> <h2>The file you uploaded is not a valid .wav file. Please try again.</h2>");
								response.end("\n</div>\n</body>\n</html>");
								exec("rm -R "+fileDir, function(error, stdout, stderr) {});
							}
						});
					}
					else {
						//File is not a valid .wav
						response.write("<h1>Error:</h1> <h2>The file you uploaded is not a valid .wav file. Please try again.</h2>");
						response.end("\n</div>\n</body>\n</html>");
						exec("rm -R "+fileDir, function(error, stdout, stderr) {});
					}
				}
				else {
					//Duplicate file upload
					response.write("<h1>Error:</h1> <h2>It looks you've already uploaded this file.<br>We'll email you when we finish demodulating it.</h2>");
					response.end("\n</div>\n</body>\n</html>");
				}
			});
		}
		
	});
}


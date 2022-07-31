
from customURLS import execute

from os import listdir
from os.path import isfile, join

SUPPORTED_METHODS = ["GET" , "POST"]

class HTTP():

    def parseHeaders(self, headers):
        output = {}
        for header in headers:
            if header == "\r\n":
                print("breaking")
                break
            
            temp = header.split(":")
            output[temp[0].strip()] = temp[1].strip()

        return output
        
    def parseGETData(self, path):
        GETData = path.split("?")
        if len(GETData) == 1:
            return {}

        GETData = GETData[1].split("&")
        output = {}
        for data in GETData:
            #TODO: convert string to int / float or whatever datatype
            temp = data.split("=")
            output[temp[0]] = temp[1].replace("%20" , " ")

        return output


    def validateHeaders(self, headers):

        if "Expect" in headers and headers["Expect"] != "100-continue":
            return 417

        return 200


    def returnOutput(self, status , path , content = None , acceptType = "html"):
        # if acceptType == "html":
        #     acceptType = "text/html"
        # elif acceptType == "image":
        #     acceptType = "image/*"

        return {
            "status" : status,
            "content" : content,
            "path" : path,
            "accept" : acceptType,
            "type" : acceptType
        }

    def generateRequestObj(self, method, path , headers,  getData = {}, postData = {}):
        return {
            "type" : method,
            "path" : path,
            "headers" : headers,
            "post" : postData,
            "get" : getData,
        }

    def serveImages(self, imageName):
        imageName = imageName[1:]
        print("image name " , imageName)
        try:
            return 200 , open("images/" + imageName , "rb").read()
        except Exception as ex:
            print("Unable to open file" , imageName , ex)
            return 404 , None
    
    def decodeRequest(self, request):
        
        acceptType = "html"

        request = request.split("\r\n")
        requestLine = request[0].split(" ")
        
        if len(requestLine) != 3:
            return 400 , None

        method = requestLine[0].upper()
        path = requestLine[1]
        pathWithoutGetData = path.split("?")[0]
        protocol = requestLine[2]

        headers = self.parseHeaders(request[1:])
        statusCode = self.validateHeaders(headers)

        if statusCode != 200:
            return self.returnOutput(statusCode , "")

        if "text/html" in headers["Accept"]:
            acceptType = "html"

        elif "image/avif" in headers["Accept"]:
            acceptType = "image"

        if method not in SUPPORTED_METHODS:
            assert 5 == 6 , "Method Type Not Implemented Yet (" + method + ")"
            
        # serving images
        if acceptType == "image" and method == "GET":
            status , content = self.serveImages(path)
            if status == 404:
                return self.returnOutput(404 , "" , "")
            return self.returnOutput(200 , path , content , "image")

        GETData = self.parseGETData(path)   
        request = self.generateRequestObj(method , pathWithoutGetData, headers , GETData)
        print("Request Obj" , request)
        
        status , content = execute(request)
        return self.returnOutput(status , pathWithoutGetData, content)











        # if method == "GET":
        #     if acceptType == "html":
        #         status , content = execute(path)
        #         return self.returnOutput(status , path , content)
        #     elif acceptType == "image":
        #         status , content = self.serveImages(path)
        #         if status == 404:
        #             return self.returnOutput(404 , "" , "")
        #         return self.returnOutput(200 , path , content , "image")
        #     else:
        #         assert 5 == 6, "Accept Type not support " + headers["Accept"]

        # elif method == "POST":
        #     if acceptType == "html":
        #         status , content = execute(path)
        #         return self.returnOutput(status, path, content)
        #     else:
        #         assert 5 == 6, "Accept Type not support " + headers["Accept"]

        # else:
        #     assert 5 == 6 , "Method Type Not Implemented Yet (" + method + ")"



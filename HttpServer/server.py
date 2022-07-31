from cgitb import reset
import socketserver
from httpHandler import HTTP
MAX_REQUEST_SIZE = 2 ** 12
HOST, PORT = "localhost", 9999
STATUS_CODE = {
    "400" : "Bad Request",
    "200" : "Sucess",
    "404" : "Not Found",
    "417" : "Expectation Failed"
}


def getResponse(code):
    if STATUS_CODE[str(code)]:
        return STATUS_CODE[str(code)]
    else:
        assert 5 == 6, "Response Code Not Implemented"
        return 400


class TPCServer(socketserver.BaseRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(MAX_REQUEST_SIZE).strip()
        # print("{} wrote:".format(self.client_address[0]))
        # print(self.data.decode())
        
        http = HTTP()
        output = http.decodeRequest(self.data.decode())

        message = getResponse(output["status"])

        contentSize = len(output["content"])

        statusLine = "HTTP/1.0" + str(output["status"]) + " " + message + "\r\n"
        response = statusLine + "Content-Length: "+ str(contentSize) + "\r\n"
        
        if output["content"] == None:
            response += "Content-Type: text/html\r\n\r\n"
            response += "<h1>hehe</h1>"
        else:
            if output["type"] == "image":
                response += "Content-Type: image/*\r\n\r\n"
                response = bytes(response , "utf-8")
                response = response + output["content"]

            elif output["type"] == "html":
                response += "Content-Type: text/html\r\n\r\n"
                response += output["content"]
                response = response.encode()
            else:
                assert 5 == 6, "Accept Type not supported server.py"

        self.request.sendall(response)

if __name__ == "__main__":

    # Create the server, binding to localhost on port 9999
    with socketserver.TCPServer((HOST, PORT), TPCServer) as server:
        print("Server Running")
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.serve_forever()
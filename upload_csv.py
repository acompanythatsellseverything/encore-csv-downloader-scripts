import os
import http.server
import cgi
import json

UPLOAD_DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class CSVUploadHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "*")
        self.send_header("Access-Control-Allow-Headers", "*")
        self.send_header("Content-type", "application/json")
        self.end_headers()

        ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
        if ctype != 'multipart/form-data':
            response = json.dumps({"status": 400, "error": "Invalid content type"})
            self.wfile.write(response.encode('utf-8'))
            self.wfile.flush()
            return

        fields = cgi.FieldStorage(fp=self.rfile, headers=self.headers, environ={'REQUEST_METHOD': 'POST'})
        
        if 'file' not in fields:
            response = json.dumps({"status": 400, "error": "No file field found in request"})
            self.wfile.write(response.encode('utf-8'))
            self.wfile.flush()
            return

        file_item = fields['file']

        if file_item.file and file_item.filename:
            file_name = os.path.basename(file_item.filename)
            file_path = os.path.join(UPLOAD_DIRECTORY, file_name)

            with open(file_path, 'wb') as output_file:
                output_file.write(file_item.file.read())

            response = json.dumps({
                "status": 200,
                "message": "File uploaded successfully",
                "filename": file_name,
                "path": file_path
            })
            self.wfile.write(response.encode('utf-8'))
            self.wfile.flush()
            print(f"Uploaded {file_name} to {file_path}")
        else:
            response = json.dumps({"status": 500, "error": "Failed to upload file"})
            self.wfile.write(response.encode('utf-8'))
            self.wfile.flush()
            print("No valid file found")

    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "*")
        self.send_header("Access-Control-Allow-Headers", "*")
        self.end_headers()

if __name__ == "__main__":
    server_address = ('', 8000)
    httpd = http.server.HTTPServer(server_address, CSVUploadHandler)
    print(f"Starting server on port {server_address[1]}, saving files to {UPLOAD_DIRECTORY}")
    httpd.serve_forever()
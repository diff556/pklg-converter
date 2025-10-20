import os
import subprocess
from flask import Flask, request, send_file, render_template_string
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = '/tmp/uploads' # Use /tmp folder which is standard for temp files
# The os.makedirs line was here. We have moved it.

# HTML for the upload page, with a cleaner look
HTML_TEMPLATE = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>PKLG to PCAPNG Converter</title>
  <style>
    body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; background-color: #eef1f5; }
    .container { background-color: white; padding: 2.5em; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); text-align: center; max-width: 90%; }
    h1 { color: #333; }
    p { color: #666; }
    input[type=file] { border: 2px dashed #ccc; padding: 2em; border-radius: 8px; cursor: pointer; display: block; width: 100%; margin: 2em 0; }
    input[type=submit] { width: 100%; padding: 12px; background-color: #007aff; color: white; border: none; border-radius: 8px; cursor: pointer; font-size: 16px; font-weight: bold; }
  </style>
</head>
<body>
  <div class="container">
    <h1>PKLG Converter</h1>
    <p>Upload your .pklg file to convert it to the standard .pcapng format.</p>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file required>
      <input type=submit value="Convert & Download">
    </form>
  </div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def upload_and_convert():
    if request.method == 'POST':
        file = request.files.get('file')
        if not file or file.filename == '': return "No file selected", 400
        
        # --- THIS IS THE NEW, SAFER LOCATION FOR MAKEDIRS ---
        # It now runs only when a file is uploaded, not at startup.
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)

        pklg_filename = secure_filename(file.filename)
        pklg_path = os.path.join(UPLOAD_FOLDER, pklg_filename)
        file.save(pklg_path)

        pcapng_filename = os.path.splitext(pklg_filename)[0] + '.pcapng'
        pcapng_path = os.path.join(UPLOAD_FOLDER, pcapng_filename)
        
        try:
            subprocess.run(['tshark', '-r', pklg_path, '-w', pcapng_path, '-F', 'pcapng'], check=True, timeout=30)
        except Exception as e:
            return f"Conversion failed. Please ensure you uploaded a valid .pklg file. Error: {e}", 500
        finally:
            if os.path.exists(pklg_path): os.remove(pklg_path)

        @app.after_request
        def cleanup(response):
            if os.path.exists(pcapng_path): os.remove(pcapng_path)
            return response
        
        return send_file(pcapng_path, as_attachment=True)

    return render_template_string(HTML_TEMPLATE)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
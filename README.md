<h1>CSV to Strapi Data Uploader</h1>
<p>These scripts provide a way to upload data from CSV files directly to Strapi via its admin API. The system consists of two main components:</p>

<ol>
  <li><strong>CSV Upload Server</strong>: A local HTTP server for handling file uploads.</li>
  <li><strong>CSV Data Processor</strong>: A script that watches a directory for CSV files, processes them, and sends the data to Strapi.</li>
</ol>

<h2>Prerequisites</h2>
<ul>
  <li>Python 3.x</li>
  <li>Strapi (v5.0.0 or higher recommended)</li>
  <li>Required Python packages (install via <code>pip install -r requirements.txt</code>):</li>
  <ul>
    <li>pandas</li>
    <li>requests</li>
    <li>python-dotenv</li>
  </ul>
  <li>Environment variables configured in a <code>.env</code> file (explained below)</li>
</ul>

<h2>Setup</h2>
<ol>
  <li>Clone or download the repository with these scripts to your local machine.</li>
  <li>Configure the <code>.env</code> file with the following variables:</li>
  <ul>
    <li><code>WATCH_DIR</code>: Directory to watch for new CSV files</li>
    <li><code>STRAPI_URL</code>: Strapi endpoint URL (e.g., <code>https://yourdomain.com/api/articles</code>)</li>
    <li><code>TOKEN</code>: Strapi API authentication token</li>
    <li><code>EVENT_TYPE_MAPPING</code>: Mappings of event type names to IDs, e.g., <code>Concert:1,Workshop:2</code></li>
  </ul>
  <li>Run the upload csv:</li>
  <pre><em>python upload_csv.py</em></pre>
  <li>This server runs on port 8000 by default and allows you to upload files to the watch directory.</li>
  <li>Start the CSV Data Processor:</li>
  <pre><em>python send_data.py</em></pre>
</ol>

<h2>Usage</h2>
<h3>1. CSV Upload Server</h3>
<p>The <code>upload_server.py</code> script starts a simple HTTP server. It can receive file uploads with a <code>POST</code> request to <code>/</code>, where the file should be attached as <code>multipart/form-data</code> with the field name <code>file</code>.</p>

<ul>
  <li>Start the server:</li>
  <pre><em>python upload_server.py</em></pre>

  <li>Upload a file via <code>POST</code> request:</li>
  <pre><em>POST http://localhost:8000/</em>
  <em>Content-Type: multipart/form-data</em>
  <em>Body:</em>
  <em>file: [CSV file]</em></pre>
</ul>
<p>The server saves files in the directory where the script is located.</p>

<h3>2. CSV Data Processor</h3>
<p>The <code>send_data.py</code> script continuously monitors the specified directory for CSV files. When a new CSV file is detected, the script:</p>
<ul>
  <li>Parses and formats the data</li>
  <li>Sends the formatted data to Strapi using the configured API endpoint</li>
  <li>Deletes the CSV file once processed</li>
</ul>

<h4>File Format</h4>
<p>The CSV should contain the following columns:</p>
<code>title, description, slug, event_type, metaTitle, metaDescription, metaKeywords, cover, stay_ahead, city, date</code>

<h4>Script Details</h4>
<ul>
  <li><strong>File Watching</strong>: The script continuously monitors <code>WATCH_DIR</code> and processes CSV files found in the directory.</li>
  <li><strong>Data Processing</strong>: Data is formatted to match Strapi's expected format. The <code>date</code> field is converted from <code>DD.MM.YYYY</code> to <code>YYYY-MM-DD</code> if provided.</li>
  <li><strong>Data Uploading</strong>: Each row is uploaded to Strapi using the API endpoint specified by <code>STRAPI_URL</code>.</li>
</ul>

<h2>Example</h2>
<p>Place your <code>.csv</code> files in the <code>WATCH_DIR</code> and run the script. The script will automatically detect, process, and upload the data to Strapi, then delete the file.</p>

<h2>Notes</h2>
<ul>
  <li>Ensure the <code>.env</code> file is configured with accurate API details.</li>
  <li>Use a reverse proxy for secure connections if deploying to a production environment.</li>
</ul>

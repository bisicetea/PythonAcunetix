# PythonAcunetix

The Acunetix Vulnerability Scanner is a Python tool that allows you to interact with the Acunetix API to perform vulnerability scans on target URLs. It utilizes the Acunetix API to trigger scans and retrieve scan results, including vulnerabilities found during the scan.

## Prerequisites

Before using the Acunetix Vulnerability Scanner, ensure you have the following:

Acunetix Vulnerability Scanner: You must have access to an Acunetix Vulnerability Scanner with a valid API key.

Python Environment: Make sure you have Python installed on your system. The tool is compatible with Python 3.

Required Libraries: Install the required Python libraries using pip: pip3 install -r requirement.txt

## Getting Started

Clone the repository:

git clone https://github.com/bisicetea/PythonAcunetix.git
cd PythonAcunetix

Create a `.env` file in the project directory and add the following environment variables:

HOST=your_acunetix_host\
PORT=your_acunetix_port\
API=your_acunetix_api_key

Replace `your_acunetix_host`, `your_acunetix_port`, and `your_acunetix_api_key` with your actual Acunetix server details and API key.

## Usage

Run the `main.py` script to initiate the vulnerability scan:

python main.py

The script will perform the following steps:

1. Create a target on Acunetix for the specified URL.
2. Trigger a scan on the created target.
3. Monitor the scan status until it is completed.
4. Retrieve the scan results, including vulnerabilities found during the scan.

## Scan Results

Once the scan is completed, the tool will display a list of vulnerabilities found during the scan. Please review these vulnerabilities and take appropriate actions to address them.
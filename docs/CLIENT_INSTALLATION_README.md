# Client PC Installation Guide

This guide explains how to run the Emotion-Based Personalized Promotion Recommendation System on a new Windows client PC.

## What You Need

- Windows 10 or Windows 11
- Internet connection for the first installation
- Python 3.10 or later installed
- This project folder copied to the client PC

## Recommended Folder Setup

Copy the full project folder to a location such as:

```text
E:\pid-assignment
```

Keep the structure intact so the app can find all files.

## Step 1: Install Python

1. Download Python from:
   https://www.python.org/downloads/
2. During installation, tick:
   - Add Python to PATH
3. Finish the installation.
4. Open PowerShell and verify:

```powershell
python --version
```

You should see Python 3.10 or newer.

## Step 2: Open the Project Folder

Open PowerShell in the project directory:

```powershell
cd E:\pid-assignment
```

If your folder is in a different location, use that path instead.

## Step 3: Create a Virtual Environment

Run:

```powershell
python -m venv .venv
```

Then activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks scripts, run this first:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Then activate again.

## Step 4: Install Dependencies

Install the required packages:

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If the network is slow, use:

```powershell
pip install --default-timeout 120 --retries 10 -r requirements.txt
```

## Step 5: Run the Frontend

Start the Streamlit app:

```powershell
streamlit run src/app.py
```

If port 8501 is already in use, run:

```powershell
streamlit run src/app.py --server.port 8502
```

or

```powershell
streamlit run src/app.py --server.port 8503
```

## Step 6: Open in Browser

After the app starts, open the local address shown in PowerShell, for example:

```text
http://localhost:8502
```

## If You Want to Use the Saved Virtual Environment

If the `.venv` folder is already included in the project copy and was created on the same Windows system, you may be able to reuse it. However, the safest option on a new client PC is to recreate the virtual environment and reinstall the packages.

## What the Client Will See

- Dark-mode modern frontend
- Live review analysis screen
- Batch CSV upload screen
- Dashboard with charts and metrics
- Promotion rule playbook
- System storyboard and sample CSV download

## Common Issues

### 1. `streamlit` is not recognized
Run Streamlit using the virtual environment Python:

```powershell
.\.venv\Scripts\python -m streamlit run src/app.py
```

### 2. `No module named streamlit`
That means dependencies are not installed in the active environment.
Run:

```powershell
pip install -r requirements.txt
```

### 3. PowerShell blocks activation
Run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

### 4. Port already in use
Run the app on another port:

```powershell
streamlit run src/app.py --server.port 8503
```

## Shutdown

To stop the app, return to the terminal running Streamlit and press:

```powershell
Ctrl + C
```

## Handover Checklist

Before handing the project to a client PC, confirm:

- Python is installed
- Dependencies install successfully
- The app starts without errors
- The browser opens the correct localhost URL
- The client can upload a CSV and view results

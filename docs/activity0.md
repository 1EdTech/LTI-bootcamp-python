# **Workshop Activity 0: Installing Prerequisites**

Before starting the workshop, make sure you have all the necessary software installed. This guide will help you set up the required tools on both **macOS** and **Windows**.

## **Prerequisites**

1. **Docker Desktop**
2. **Python** with `pipenv`
3. **TailwindCSS CLI**
4. **Node.js** (to run `npx`)
5. **Code Editor** (VS Code recommended)
6. **Administrator Access** (to update the hosts file)

### **Note**:
You will need **administrator access** on your machine to update the hosts file.

---

## **1. Docker Desktop**

Docker Desktop is required to run the workshop environment using containers.

### **macOS Installation**:
1. Download Docker Desktop from the [Docker website](https://www.docker.com/products/docker-desktop).
2. Open the `.dmg` file and drag Docker to your Applications folder.
3. Launch Docker from your Applications folder.
4. Follow the instructions to complete the installation.

### **Windows Installation**:
1. Download Docker Desktop from the [Docker website](https://www.docker.com/products/docker-desktop).
2. Run the installer and follow the prompts.
3. Restart your computer if prompted.

### **Verify Installation**:
To check if Docker is installed correctly, open a terminal (macOS) or PowerShell (Windows) and run:

```bash
docker --version
```

---

## **2. Python with Pipenv**

Pipenv is used to manage Python environments and dependencies.

### **macOS Installation**:
1. Install Python 3 from [python.org](https://www.python.org/downloads/).
2. Open a terminal and install Pipenv:

```bash
brew install pipenv
```

If you don’t have Homebrew installed, you can install it from [brew.sh](https://brew.sh/).

### **Windows Installation**:
1. Download Python 3 from [python.org](https://www.python.org/downloads/).
2. During installation, ensure that **"Add Python to PATH"** is checked.
3. Open PowerShell and install Pipenv:

```bash
pip install --user pipenv
```

### **Verify Installation**:
To check if Pipenv is installed correctly, run:

```bash
pipenv --version
```

---

## **3. TailwindCSS CLI**

TailwindCSS is a utility-first CSS framework which some of the samples use. You may need its CLI for the workshop..

### **macOS & Windows Installation**:
1. Open your terminal (macOS) or PowerShell (Windows).
2. Install the TailwindCSS CLI globally using `npm`:

```bash
npm install -g tailwindcss
```

### **Verify Installation**:
To check if TailwindCSS is installed correctly, run:

```bash
tailwindcss --version
```

---

## **4. Node.js (with npx)**

Node.js is required to run JavaScript-based tools like `npx`.

### **macOS & Windows Installation**:
1. Download Node.js (LTS version) from [nodejs.org](https://nodejs.org/).
2. Install it by following the prompts.

### **Verify Installation**:
To check if Node.js and `npx` are installed correctly, run:

```bash
node --version
npx --version
```

---

## **5. Code Editor**

Bring your favorite code editor to the workshop. We recommend using **Visual Studio Code (VS Code)** for the best experience.

### **Download VS Code**:
- Download it from [code.visualstudio.com](https://code.visualstudio.com/).

VS Code supports extensions for both Python and Node.js development, making it a versatile editor for this workshop.

---

## **6. Administrator Access to Update Hosts File**

You will need administrator access to modify the `hosts` file on your machine. This is necessary to map the workshop domains (`platform.ltitraining.net` and `tool.ltitraining.net`) to your local environment.

- **On macOS**: You can modify the `hosts` file by opening the terminal and running:

```bash
sudo nano /etc/hosts
```

- **On Windows**: You will need to open Notepad as an administrator and edit the file located at:

```
C:\Windows\System32\drivers\etc\hosts
```

Make sure to add the following lines to the `hosts` file:

```
127.0.0.1 platform.ltitraining.net
127.0.0.1 tool.ltitraining.net
```

---

## **Summary**

Ensure that the following tools are installed:
- Docker Desktop
- Python 3 with Pipenv
- TailwindCSS CLI
- Node.js (with npx)
- A code editor (VS Code recommended)
- Administrator access to modify the hosts file

Once everything is installed, you’re ready to proceed to the next activity where we’ll set up the Docker environment.
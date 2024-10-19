# **Working with the Workshop Files**

This document provides instructions for working with the workshop files, managing Docker containers, cleaning up volumes, and using the Python and TailwindCSS environments.

---

## **1. Managing Docker Containers**

This project uses Docker Compose to set up and manage the environment. Here are the essential Docker commands for starting, stopping, and cleaning up the environment.

### **Starting the Environment**

To start the Docker containers for Moodle, MariaDB, and Nginx, run the following command from the `environment/` directory:

```bash
docker-compose up -d
```

This command will:
- Build the services if they are not already built.
- Start the containers in the background (detached mode).

### **Stopping the Environment**

To stop the running containers without removing the volumes (i.e., without losing data):

```bash
docker-compose stop
```

This will gracefully stop the containers, but the data will remain persisted.

### **Cleaning Up the Environment**

If you want to remove the containers and clean up the associated data (volumes), run:

```bash
docker-compose down --volumes
```

This will stop the containers and delete the associated volumes, meaning any persisted data (e.g., Moodle database) will be removed.

---

## **2. Hosts File Management**

### **Updating the Hosts File**

To ensure the domains `platform.ltitraining.net` and `tool.ltitraining.net` resolve to your local environment, make sure your `/etc/hosts` file is updated.

#### **On macOS/Linux**:
Open the `/etc/hosts` file in a text editor with administrator privileges:

```bash
sudo nano /etc/hosts
```

See [Activity 1](activity1.md) for more details

---

## **3. Working with the Python Environment**

This project uses **Pipenv** to manage Python dependencies. Here's how to start the environment and run the code.

### **Starting the Pipenv Environment**

1. Navigate to the root directory of the project.
2. Run the following command to activate the environment:

```bash
pipenv shell
```

This will activate the virtual environment with all necessary dependencies.

### **Running the Python Code**

Once inside the Pipenv environment, you can run the Flask app or any other Python scripts. For example, to run the Flask app:

```bash
python exercise4/app.py
```

---

## **4. TailwindCSS: Running `npx` in Watch Mode**

If you need to modify or regenerate the CSS, you can run TailwindCSS in watch mode. This allows you to automatically generate new CSS when changes are made.

### **Running TailwindCSS in Watch Mode**

To run TailwindCSS in watch mode:

1. Navigate to the `exercise4/` directory:

```bash
cd exercise4
```

2. Run the following command:

```bash
npx tailwindcss -i ./static/css/input.css -o ./static/css/output.css --watch
```

This will watch the `input.css` file for changes and regenerate `output.css` as you modify the styles.

### **Optional Dependency**

Since the `output.css` file is already included in the sample code, **Node.js and TailwindCSS are optional dependencies**. You only need to run this step if you're modifying the CSS styles.

---

## **5. Cleaning Up Data**

If you want to completely reset the environment, including removing any persisted data, follow these steps:

1. **Stop the Docker containers**:
   ```bash
   docker-compose stop
   ```

2. **Remove the containers and volumes**:
   ```bash
   docker-compose down --volumes
   ```

3. **Update or clean the hosts file** (if necessary) to remove any entries related to `platform.ltitraining.net` and `tool.ltitraining.net`.

---

## **Summary**

This document covers:
- Managing Docker containers (`up`, `stop`, `down` with volumes).
- Updating the `hosts` file for proper domain resolution.
- Starting the Pipenv environment and running Python code.
- Running `npx tailwind` in watch mode to regenerate CSS.
- Cleaning up persisted data and volumes.

Make sure to refer back to this document when working with the project during the workshop.


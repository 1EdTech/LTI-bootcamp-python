# **Quick Checklist for Workshop Setup**

After setting up your environment, run the following quick tests to ensure everything is working correctly. These tests will verify that everythng is running as expected.

---

## **1. Docker and Moodle Environment**

### **Test 1: Verify Docker Containers**

First, ensure that all the Docker containers (Moodle, MariaDB, Nginx) are running correctly.

1. In the terminal or PowerShell, navigate to the `environment/` directory.
2. Run the following command to check the status of the Docker containers:

```bash
docker-compose ps
```

You should see the status as `Up` for the Moodle, MariaDB, and Nginx containers. For example:

```bash
    Name                Command          State             Ports
---------------------------------------------------------------------
nginx-proxy   /docker-entrypoint.sh ngin ...   Up      0.0.0.0:443->443/tcp
mariadb       /opt/bitnami/scripts/mari ...   Up      3306/tcp
platform.dev  /opt/bitnami/scripts/mood ...   Up      8080/tcp
```

If the containers are not running, use `docker-compose up` to start them.

---

### **Test 2: Access Moodle**

1. Open your browser.
2. Navigate to the following URL:

```
https://platform.ltitraining.net
```

You should see the Moodle login page. If the page doesn’t load, double-check that the containers are running, and ensure that your `/etc/hosts` file is correctly configured to resolve `platform.ltitraining.net` to `127.0.0.1`.

---

## **2. Python and Pipenv Environment**

### **Test 3: Verify Python Environment**

1. In the terminal or PowerShell, activate the Python environment with Pipenv:

```bash
pipenv shell
```

2. Once inside the environment, verify that Python is working by running:

```bash
python --version
```

This should return the Python version, confirming that the environment is correctly set up.

---

### **Test 4: Run the Python Code**

Navigate to the `exercise4/` directory and run the Flask app (or another Python script) to ensure everything is working:

```bash
cd exercise1
python app.py
```

You should see the Flask app running, and it will provide a URL (typically `http://127.0.0.1:3000/`) where you can access the app in your browser.

---


## **Summary of Quick Tests**:
- **Test 1**: Check Docker container status.
- **Test 2**: Access Moodle via `https://platform.ltitraining.net`.
- **Test 3**: Verify the Python environment.
- **Test 4**: Run the Python Flask app.

Running through these tests will ensure that everything is correctly set up and functioning for the workshop.
# Workshop Activity 1: 

## Setting Up the Git Repository and Docker Environment

### Objective:

![Topology](images/topology.png)

By the end of this activity, you will have cloned the workshop's git repository and created the Docker environment to run a Learning Platform.  We will be using an opensource Learning Management Platform (LMS) called Moodle.  During this Bootcamp we will develop an LTI Tool that will integrate into any mainstream LMS platform via LTI 1.3.

### Prerequisites:
- Basic knowledge of Git and Docker.
- Docker and Docker Compose installed on your machine.
- Access to modify the local `/etc/hosts` file (administrator privileges may be required).

See the [Guide for setting up the prerequisites](activity0.md) if you need further assistance.

---

### **Steps to Follow:**

#### 1. **Clone the Git Repository**

Start by cloning the workshop repository to your local machine.

```bash
git clone https://github.com/1EdTech/LTI-bootcamp-python.git
```

This will download all the necessary files, including the configurations for the Docker environment.

#### 2. **Navigate to the Environment Directory**

Once the repository is cloned, navigate to the `environment/` directory where the Docker configuration files are located.

```bash
cd environment
```

#### 3. **Update the Local Hosts File**

In this setup, we will use 2 real domains with real (browser-trusted) SSL certificates.  We will configure the routing on your PC to route these domains locally within your machine.  This allows us to focus on LTI development without the complexities of browser security getting in the way.

To ensure that the domains `platform.ltitraining.net` and `tool.ltitraining.net` resolve to your local environment, you need to update your local `/etc/hosts` file.

##### **On macOS/Linux**:
1. Open the `/etc/hosts` file in your text editor with administrator privileges:

   ```bash
   sudo nano /etc/hosts
   ```

2. Add the following lines to the file:

   ```bash
   127.0.0.1 platform.ltitraining.net tool.ltitraining.net
   ```

3. Save and close the file.

##### **On Windows**:
1. Open Notepad as an administrator (right-click and choose "Run as Administrator").
2. Open the `hosts` file located at `C:\Windows\System32\drivers\etc\hosts`.
3. Add the following lines at the end of the file:

   ```bash
   127.0.0.1 platform.ltitraining.net tool.ltitraining.net
   ```

4. Save and close the file.

This step ensures that your browser correctly resolves these domains to your local machine when you access them.

#### 4. **Start the Docker Environment**

Once you’ve reviewed the configurations, start the Docker containers using Docker Compose. This will spin up Moodle, MariaDB, and Nginx services.

```bash
docker-compose up --build
```

This command will:
- Build and start all the services defined in the `docker-compose.yml` file.
- Configures and runs the services 
- Please note:  This may take a few mins to complete the first time.


#### 5. **Run through the Checklist**

To verify that everything is running correctly, complete the checks the [Checklist](checklist.md)

---

### **Troubleshooting:**

- **Containers not starting**: If the containers fail to start, check the logs with the following command:

  ```bash
  docker-compose logs
  ```

  Look for any error messages that indicate issues with the configuration or missing dependencies.

- **Cannot access platform.ltitraining.net**: Ensure that the `/etc/hosts` file is correctly set to resolve `platform.ltitraining.net` and `tool.ltitraining.net` to `127.0.0.1`.

- **SSL issues**: If you run into SSL certificate issues, ensure that the certificates in the `certs/` folder are correctly mapped in the `nginx.conf` file.

---

### **Questions &  Common Tasks:**

To understand how to start, stop, reset, clean up,  details are outlined in the [Common Tasks Document](common_tasks.md)

---

### **Activity Summary:**
You have now cloned the repository, updated your hosts file, started the Docker environment, and accessed Moodle via the `platform.ltitraining.net` domain. You are ready to move on to the next activity, where you will configure the Moodle LTI tool and begin developing.



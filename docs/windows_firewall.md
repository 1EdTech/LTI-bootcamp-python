## Windows Firewall

You may find that Windows Firewall blocks the traffic between the NGINX Proxy server and Moodle. 

To allow Moodle to run on Windows without being blocked by the firewall, you can add an exception for Docker's services, which includes the port that Moodle is running on. Here's how you can do it:

### **Steps to Add a Firewall Exception for Moodle in Windows**

1. **Open Windows Firewall**:
   - Press `Windows + S` and type `Windows Defender Firewall`, then select **Windows Defender Firewall with Advanced Security**.

2. **Add a New Inbound Rule**:
   - In the left sidebar, click on **Inbound Rules**.
   - In the right sidebar, click on **New Rule**.

3. **Create a Port Rule**:
   - Choose **Port** as the type of rule and click **Next**.
   - Select **TCP**.
   - In the "Specific local ports" field, enter the port number that Moodle is running on. Typically, Moodle runs on port **8080** or another port that you have configured in Docker. Enter that number and click **Next**.

4. **Allow the Connection**:
   - On the next screen, select **Allow the connection** and click **Next**.

5. **Apply the Rule**:
   - Choose when this rule applies. You can select:
     - **Domain** (if your computer is part of a domain)
     - **Private** (for home or private networks)
     - **Public** (for public networks)
   - Click **Next**.

6. **Name the Rule**:
   - Give the rule a descriptive name like "Moodle Docker Exception".
   - Click **Finish**.

7. **Repeat for Outbound Rule** (Optional):
   - You can also add an outbound rule for the same port if needed by following the same steps under **Outbound Rules**.

### **Alternative: Allow Docker Application through Firewall**

If you prefer, you can allow the Docker application through the firewall, which will cover any ports that Docker containers (like Moodle) use.

1. **Open Windows Firewall**:
   - Press `Windows + S` and type `Windows Defender Firewall`, then select **Allow an app or feature through Windows Defender Firewall**.

2. **Allow Docker Desktop**:
   - Scroll through the list of apps and look for **Docker Desktop**.
   - Ensure that both **Private** and **Public** boxes are checked for Docker Desktop.
   - Click **OK** to save the changes.

This should allow Moodle to run through Docker without being blocked by the Windows firewall. 

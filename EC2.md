Here’s a step-by-step guide to running your **genx3D** project in production on an AWS EC2 instance (or any cloud VM):

---

## 1. **Launch an EC2 Instance**
- Use the AWS Console to launch an instance (Ubuntu 22.04 LTS is recommended).
- Choose a size (t3.medium or larger for CAD/AI workloads).
- Allow inbound ports: **22** (SSH), **8000** (your app), and **80/443** (if using a reverse proxy).
- Add your SSH key.

---

## 2. **Connect to Your Instance**
```bash
ssh -i /path/to/your-key.pem ubuntu@<EC2_PUBLIC_IP>
```

---

## 3. **Install Docker**
```bash
sudo apt-get update
sudo apt-get install -y docker.io
sudo systemctl enable --now docker
sudo usermod -aG docker $USER
# Log out and back in to use docker without sudo
```

---

## 4. **Clone Your Repo**
```bash
git clone https://github.com/yourusername/genx3D.git
cd genx3D
```

---

## 5. **Set Up Your Environment**
- Create a `.env` file in the project root with your secrets:
  ```
  OPENROUTER_API_KEY=your_openrouter_key
  # Add any other required environment variables
  ```

---

## 6. **Build and Run the Docker Container**
```bash
docker build -t genx3d .
docker run -d --env-file .env -p 8000:8000 genx3d
```

---

## 7. **Access the App**
- In your browser, go to:  
  `http://<EC2_PUBLIC_IP>:8000/app/`

---

## 8. **(Recommended) Set Up a Reverse Proxy (Nginx) for HTTPS**
- Install Nginx:
  ```bash
  sudo apt-get install -y nginx
  ```
- Configure Nginx to proxy requests to `localhost:8000` and set up SSL (Let’s Encrypt).
- Open ports 80 and 443 in your EC2 security group.

---

## 9. **(Optional) Set Up Docker Compose for Easier Management**
- Create a `docker-compose.yml` (let me know if you want a template).

---

## 10. **(Optional) Set Up Auto-Start**
- Use a systemd service or Docker restart policies (`--restart always`) to keep your app running after reboot.

---

### **Summary Table**

| Step                | Command/Action                                      |
|---------------------|-----------------------------------------------------|
| Connect SSH         | `ssh -i ... ubuntu@<EC2_PUBLIC_IP>`                 |
| Install Docker      | `sudo apt-get install -y docker.io`                 |
| Clone repo          | `git clone ...`                                     |
| Set up .env         | Add secrets to `.env`                               |
| Build image         | `docker build -t genx3d .`                          |
| Run container       | `docker run -d --env-file .env -p 8000:8000 genx3d` |
| Access app          | `http://<EC2_PUBLIC_IP>:8000/app/`                  |

---

**Let me know if you want:**
- A sample Nginx config for HTTPS
- A `docker-compose.yml`
- A systemd service file for auto-start
- Any troubleshooting help

Just say the word!

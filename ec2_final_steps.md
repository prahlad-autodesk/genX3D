Here is the **modified deployment guide for your blog**, assuming your Dockerized app runs on port `8000/blog` and your domain is `https://prahlad.blog`.

---

## ✅ 1. **Launch EC2 Instance**

* Launched **Ubuntu EC2 instance** (Free tier eligible).
* Configured **Security Group**:

  | Port | Purpose        |
  | ---- | -------------- |
  | 22   | SSH            |
  | 80   | HTTP           |
  | 443  | HTTPS          |
  | 8000 | Optional (dev) |

---

## ✅ 2. **Install Required Packages**

```bash
sudo apt update
sudo apt install -y docker.io docker-compose nginx certbot python3-certbot-nginx
sudo systemctl enable docker
```

---

## ✅ 3. **Pull & Run Docker Image**
`
Assuming your blog app is exposed at `/blog` on port 8000 inside the container:

```bash
# Pull your image from DockerHub
docker pull ps2program/genx3d

# Run it on host port 8000
docker run -d -p 8000:8000 --name prahlad_blog ps2program/genx3d

docker run -d -p 8000:8000 ps2program/genx3d:v1.1.2


docker run -d -p 8000:8000 \
  --name prahlad_blog_v2 \
  -e OPENAI_API_KEY="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" \
  ps2program/genx3d:v1.1.2



```

---

## ✅ 4. **Point Your Domain to EC2 Public IP**

In your domain provider's DNS settings (e.g., Hostinger), add:

| Type | Name | Value           | TTL |
| ---- | ---- | --------------- | --- |
| A    | @    | `EC2_PUBLIC_IP` | 600 |
| A    | www  | `EC2_PUBLIC_IP` | 600 |

Then verify DNS is resolving:

```bash
nslookup prahlad.blog
```

---

## ✅ 5. **Configure Nginx Reverse Proxy**

Edit default Nginx config:

```bash
sudo nano /etc/nginx/sites-available/default
```

Update with:

```nginx
server {
    listen 80;
    server_name prahlad.blog www.prahlad.blog;

    location /blog/ {
        proxy_pass http://localhost:8000/blog/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

Test and reload:

```bash
sudo nginx -t
sudo systemctl reload nginx
```

---

## ✅ 6. **Install and Enable HTTPS with Certbot**

Run:

```bash
sudo certbot --nginx -d prahlad.blog -d www.prahlad.blog
```

Certbot will:

* Obtain SSL certificate
* Update Nginx config to redirect HTTP → HTTPS
* Set up auto-renew cron job

Test:

```bash
https://prahlad.blog/blog/
```

---

## ✅ 7. **Verify Everything Works**

* ✅ `docker ps` → container is running
* ✅ `curl http://localhost:8000/blog/` → working
* ✅ `curl https://prahlad.blog/blog/` → 200/307
* ✅ Nginx reverse proxying `/blog/`
* ✅ SSL valid in browser

---

## 🔒 Optional: Set Up Auto-Restart for Docker on Reboot

```bash
docker update --restart unless-stopped prahlad_blog
```

---

## 🚀 Summary Checklist

| Step                        | Done |
| --------------------------- | ---- |
| EC2 running + SG setup      | ✅    |
| Docker + Nginx installed    | ✅    |
| Blog container running      | ✅    |
| Domain pointing to EC2      | ✅    |
| Nginx reverse proxy working | ✅    |
| HTTPS installed via Certbot | ✅    |
| Blog reachable via HTTPS    | ✅    |

---

Let me know if you'd like to:

* Use **`docker-compose`** for clean deployments.
* Auto-deploy via **GitHub Actions** or **CI/CD**.
* Add **basic auth** or **rate-limiting** to your blog.

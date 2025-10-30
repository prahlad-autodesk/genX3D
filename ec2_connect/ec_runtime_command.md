Sure! Here’s the list of all the commands we used step-by-step in your EC2 setup and troubleshooting:

---

### 1. Check disk usage

```bash
df -h
```

---

### 2. Check block devices and partitions

```bash
lsblk
```

---

### 3. Grow the partition to use all free space

```bash
sudo growpart /dev/nvme0n1 1
```

---

### 4. Resize the filesystem to fill the grown partition

```bash
sudo resize2fs /dev/nvme0n1p1
```

---

### 5. Verify updated disk space

```bash
df -h /
```

---

### 6. Add `ubuntu` user to `docker` group to avoid using `sudo` with docker

```bash
sudo usermod -aG docker ubuntu
```

*(Remember to log out and back in for this to take effect)*

---

### 7. Pull docker image (with or without sudo)

```bash
docker pull ps2program/genx3d:latest
```

or

```bash
sudo docker pull ps2program/genx3d:latest
```

---

### 8. Cleanup Docker system (optional, if you want to free space)

```bash
sudo docker system prune -a
```

---

### 9. Cleanup apt cache (optional)

```bash
sudo apt-get clean
```

---

If you want me to create a full script or checklist to automate these or for future use, just ask!

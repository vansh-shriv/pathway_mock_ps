# 🐳 Pathway Library using Docker (Linux Environment on Windows)

## 📘 Objective  
The Pathway library only works in Linux environments. Since the team uses Windows, we use **Docker** to create a consistent Linux-based development setup.  

---

## 🧩 Task Breakdown  

### **Task 1 — Install Docker Desktop**  
- Installed **[Docker Desktop](https://www.docker.com/products/docker-desktop/)** on Windows.  
- Verified installation using:  
  ```bash
  docker --version
  ```
- Docker Desktop allows running Linux containers natively on Windows.

---

### **Task 2 — Deploy Docker for a Pathway Application**  
Created a **Dockerfile** to containerize a simple Pathway program.

#### **Project Structure**
```
pathway-docker/
│
├── Dockerfile
└── main.py
```

#### **main.py**
```python
import pathway as pw

# A simple example using Pathway
table = pw.debug.table_from_markdown("""
    a | b
    1 | 2
    3 | 4
    5 | 6
""")

result = table.reduce(sum_a=pw.reducers.sum(table.a), sum_b=pw.reducers.sum(table.b))
pw.debug.compute_and_print(result)
```

#### **Dockerfile**
```Dockerfile
# Use an official Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install the Pathway library
RUN pip install --no-cache-dir pathway

# Copy files into container
COPY . /app

# Run the script
CMD ["python", "main.py"]
```

#### **Build the Docker image**
```bash
docker build -t pathway-app .
```

---

### **Task 3 — Execute Pathway Program inside Docker**
Run the container:
```bash
docker run --rm pathway-app
```

**Expected Output:**
```
sum_a | sum_b
9     | 12
```

This confirms that the Pathway program successfully runs inside a Linux container — even on Windows.

---

## ✅ Outcome  
| Task | Description | Status |
|------|--------------|--------|
| (1) | Install Docker Desktop | ✅ Completed |
| (2) | Create and deploy Docker setup for Pathway | ✅ Completed |
| (3) | Run Pathway code inside container | ✅ Completed |

---

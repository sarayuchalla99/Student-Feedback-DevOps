# Student Feedback System — DevOps Case Study

This starter project includes a Flask web app with three pages, Docker, Kubernetes manifests, and a Jenkins pipeline template.

## Pages
- `/` Home page
- `/feedback` Submit feedback
- `/dashboard` View feedback and average rating
- `/health` Kubernetes health-check endpoint

## 1. Run locally (Windows PowerShell)
Open a terminal in this folder:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5000. If PowerShell blocks activation, run:
`Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`

## 2. Run with Docker
Start Docker Desktop first:

```powershell
docker build -t student-feedback:local .
docker run --rm -p 5000:5000 student-feedback:local
```

Open http://localhost:5000.

## 3. Upload to GitHub
Create an empty GitHub repository, then replace the URL below with your own:

```powershell
git init
git add .
git commit -m "Initial Student Feedback System"
git branch -M main
git remote add origin https://github.com/YOUR_GITHUB_USERNAME/YOUR_REPOSITORY.git
git push -u origin main
```

If `origin` already exists, use `git remote set-url origin YOUR_REPOSITORY_URL`.

## 4. Docker Hub
Create a Docker Hub repository named `student-feedback`, sign in, then run:

```powershell
docker login
docker build -t YOUR_DOCKERHUB_USERNAME/student-feedback:latest .
docker push YOUR_DOCKERHUB_USERNAME/student-feedback:latest
```

Replace the placeholder username in both `deployment.yaml` and `Jenkinsfile`.

## 5. Kubernetes
Ensure a cluster is running and `kubectl` is configured. For Docker Desktop Kubernetes:

```powershell
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
kubectl get pods
kubectl get services
```

When pods are running, try http://localhost:30080. Otherwise use:
`kubectl port-forward service/student-feedback-service 5000:5000`
and open http://localhost:5000.

## 6. Jenkins CI/CD setup
This Jenkinsfile is a template and needs Jenkins credentials and compatible tools configured.

The Jenkins agent must have Git, Docker access, `kubectl`, and network access to the target cluster. The supplied pipeline uses Linux `sh` commands; use a Linux Jenkins agent or adapt commands for Windows.

In **Manage Jenkins → Credentials**, create:
1. Username/password credential ID `dockerhub-credentials`. Use your Docker Hub username and a Docker Hub access token.
2. Secret file credential ID `kubeconfig-file`. Upload a kubeconfig file authorized for the cluster.

Replace `YOUR_DOCKERHUB_USERNAME` in `Jenkinsfile`. Create a Pipeline job linked to the GitHub repository, with script path `Jenkinsfile`.

To trigger automatically on pushes, configure a GitHub webhook to your reachable Jenkins URL ending in `/github-webhook/`, and enable **GitHub hook trigger for GITScm polling** in the job. A Jenkins server running only on your laptop is not reachable by GitHub without an appropriate network setup.

## Important notes
- SQLite data is stored inside the app/container in this learning starter. Replacing containers can reset feedback data; a production multi-replica system should use a persistent database.
- Never commit passwords, access tokens, or kubeconfig files to GitHub.
- Replace all `YOUR_...` placeholders before deploying.
- For your report, capture screenshots of the three pages, Docker build/run, Kubernetes pods/service, Jenkins success, and a build triggered by a GitHub push.

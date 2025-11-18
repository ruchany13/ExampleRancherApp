# ExampleRancherApp
In this repo include Rke2, Rancher installatin with ansible and bash. Also, example app will deploy to cluster with actiona.

File Directory:
- **Ansible:** There are Ansible Playbooks for RKE2 and Rancher Installation.
- **app:** There is an example app codes named Parentinfo written with Django. This app taken from my https://github.com/ruchany13/ParentInfoSystem-Django repo.
- **BashScripts:** There are Bash Scripts for RKE2 and Rancher Installation. Use *.conf* file for varibales.
- **Docker:** There are Dockerfiles for Develeopment and Production for app. Github CI pipelines uses this Dockerfiles.
- **K8S:** There are example Kubernetes manifests for app.
- **rancher-app-chart:** There is a Helm chart for deploy app to Kubernetes. You can reach to chart https://github.com/ruchany13/ExampleRancherApp/pkgs/container/helm-charts%2Francher-app-chart .
- **.github:** There are pipelines for Docker image build from app and Helm chart package and push both of them to specific GHCR repository

With using this repo, can build fully functional Rancher with RKE2 and deploy an example app using CI/CD. For CD use Fleet in Rancher.

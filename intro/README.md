# DE_Zoomcamp2024

#### setup codespaces. jupyter & pgsql in docker tryouts
1. Setup GitHub repository.
2. Create Codespace (your repo + 2 core).
3. Open Codespace in VSCode.
4. Install jupyter.
```bash
pip install jupyter
```
5. Open jupyter server GUI in web-browser.
6. Create docker network.
```bash
docker network create pg-network
```
7. Create docker volume.
```bash
docker volume create --name dtc_postgres_volume_local -d local
```
8. Run docker container with pgsql.
```bash
docker run -it -e POSTGRES_USER="root" -e POSTGRES_PASSWORD="root" -e POSTGRES_DB="ny_taxi" -v dtc_postgres_volume_local:/var/lib/postgresql/data -p 5432:5432 --network=pg-network --name pg-database postgres:13
```
9. Run docker container with pgadmin.
```bash
docker run -it \
    -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
    -e PGADMIN_DEFAULT_PASSWORD="root" \
    -p 8080:80 \
    --network=pg-network \
    --name pgadmin \
    dpage/pgadmin4
```
10. Install terraform. https://developer.hashicorp.com/terraform/install#Linux

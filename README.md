# Setting up the API Endpoints

This README provides instructions for setting up the database, configuring users, and connecting the client and server in development mode.

First, clone the repository and navigate to the project directory.

```bash
git clone org-184059057@github.com:hellowhorl/whorl-server.git
```

## Setup a Virtual Environment

Here you will utilize `venv`, which is short for virtual environment, specific for your client.

1. **Create a Virtual Environment**  
    - In the root of the `whorl-server` repository, run the following command:

      ```bash
      python -m venv .venv
      ```

2. **Activate the Virtual Environment**  
    - Activate your virtual environment with the command:

      ```bash
      source .venv/bin/activate
      ```

## Development Install

Once your virtual environment is set up, perform a development install by running the following command:

```bash
python -m pip install -e .
```

## Keys and Environment Variables

If you are part of the `whorl` organization, you can find the keys in the `.env` file. If you are not, you can create your own `.env` file in the root of the `whorl-server` repository.

- The `.env` file should contain the following variables:

     ```plaintext
      API_URL=localhost
      API_DB_HOST=localhost
      API_DB_USER=<your_api_db_user_name>
      API_DB_PASS=<your_api_db_pass>
      API_HOST=<your_api_host>

      OPEN_AI_KEY=<your_openai_key>

      OPENWEATHER_API=<your_openweather_key>
      OPENWEATHER_LAT=<your_openweather_latitude>
      OPENWEATHER_LON=<your_openweather_longitude>
     ```

## PostgreSQL Setup

1. **Install PostgreSQL**  
   - Make sure PostgreSQL is installed on your machine.  
   - If not installed, you can download it from [PostgreSQL Downloads](https://www.postgresql.org/download/) and follow the installation instructions for your operating system.

### MacOS

1. **Start the services**
    - Start the PostgreSQL service:

      ```bash
        brew services start postgresql
      ```

2. **Access the PostgreSQL Shell**  
   - Open a terminal and log into the PostgreSQL shell:  

     ```bash
     psql postgres
     ```

3. **To stop the service**

    - To stop the PostgreSQL service

      ```bash
        brew services stop postgresql 
      ```

### Linux

1. **Start the services**

    - Start the PostgreSQL service:

      ```sudo
      sudo systemctl start postgresql
      ```

    - Verify if PostgreSQL is running:

      ```sudo
      sudo systemctl status postgresql
      ```

    - Stop PostgreSQL when needed:

      ```sudo
      sudo systemctl stop postgresql
      ```

2. **Access the PostgreSQL Shell**  
   - Open a terminal and log into the PostgreSQL shell:  

     ```sudo
      sudo -i -u postgres psql
     ```

### Windows

1. **Start the services**

- Start the PostgreSQL service using the Services Manager:
- press Win + R, type services.msc, and press Enter.
- Locate the PostgreSQL service in the list.
- Right-click on it and choose start.

- If wanted to run alternatively you can start the service in the terminal using the command prompt:
  
  ```net
  start postgresql-x64-<version>
  ```

2. **Access the PostgreSQL Shell**  
   - Open a terminal and log into the PostgreSQL shell:
   - navigate to the PostgreSQL bin directory (e.g., C:\Program Files\PostgreSQL\<version>\bin).
   - log into the PostgreSQL shell:

     ```sudo
     psql -U postgres
     ```

3. **To Stop the Services:**

   - To stop the service:

     ```net
     stop postgresql-x64-<version>
     ```

## Database Setup

1. **Ensure PostgreSQL shell is running**

- Make sure you do the above instrsuctions because none of the database steps are doable without a PostgreSQL shell

2. **Create the Database**

   - Run the following SQL command to create the `<database>` database:

     ```sql
     CREATE DATABASE "<database>";
     ```

3. **Create the User**
    - Run the following SQL command to create the user with password (reference the `.env file` for the password):

        ```sql
        CREATE USER 'user' WITH PASSWORD '<password>';
        ```

    PS: 'user' doesn't need quotes, but 'password' does.

4. **Grant User Permissions**

   - Grant all privileges on the `<database>` database to the user:  

    ```sql
    GRANT ALL PRIVILEGES ON DATABASE "<database>" TO <user>;
    ```

5. **Verify Ownership**

   - Use the `\l` command to list databases and check if user owns the `<database>` database.  
   - If not, update the owner with this command:

     ```sql
     ALTER DATABASE "<database>" OWNER TO <user>;
     ```

6. **Exit the PostgreSQL Shell**

   - Type `\q` to exit.

## Test if client and server are connected

1. **Client Configuration**  
   - Open the `.env` file in the client directory.  
   - Set the `API_URL` to:  

     ```plaintext
     http://localhost
     ```

2. **Start the Server**  
   - Navigate to the server directory.

     ```bash
     cd src
     ```

   - Run the following command to start the server:

     ```bash
     python manage.py runserver
     ```

3. **Run the Client**  
   - In the client directory, run the command to see if output is displayed:

     ```bash
     climate
     ```

## Prometheus Setup

Prometheus is used to monitor the application by collecting metrics and providing a queryable interface for analysis. It views logs in Universal Time and integrates with Django to expose metrics.

### Steps to Set Up Prometheus

1. **Access Prometheus Dashboard**  
   - Open your browser and navigate to:

     ```text
     http://localhost:9090
     ```

2. **Query Metrics**  
   - Use the Prometheus query interface to view metrics. For example:
     - To view the number of HTTP requests before middleware creation:

       ```plaintext
       django_http_requests_before_middlewares_created
       ```

3. **Visualize Metrics**  
   - Use Prometheus' built-in graphing tools for visualizations.

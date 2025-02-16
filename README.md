
# TSI Distributed Systems Project

This repository contains the code and resources for the Distributed Systems course project. The project focuses on implementing a Remote Procedure Call (RPC) system using Python, with features like SSL-secured communication, caching, and parallel processing.

## 🚀 Features

- **Remote Procedure Call (RPC):** Implement a client-server architecture for remote method invocation.
- **SSL Encryption:** Secure communication between the client and server using SSL/TLS.
- **Caching:** Cache results of expensive operations (e.g., multiplication) to improve performance.
- **Parallel Processing:** Use multiprocessing to handle computationally intensive tasks (e.g., prime number checking).
- **Streamlit Dashboard:** Visualize logs and results using a Streamlit app.

## 🛠️ Setup and Installation

### Prerequisites
- Python 3.9 or higher
- pip for installing dependencies

### Steps

1. Clone the repository:

    ```bash
    git clone https://github.com/YuryOAraujo/TSI-Distributed-Systems.git
    cd TSI-Distributed-Systems
    ```

2. Create a virtual environment:

    ```bash
    python -m venv myenv
    ```

3. Activate the virtual environment:

    - On Windows:

      ```bash
      myenv\Scriptsctivate
      ```

    - On macOS/Linux:

      ```bash
      source myenv/bin/activate
      ```

4. Install dependencies:

    ```bash
    pip install -r Aula_8_RPC/requirements.txt
    ```

## 🖥️ Running the Project

1. **Start the DNS Server**  
   The DNS server is used for service discovery. Run it using:

    ```bash
    python Aula_8_RPC/rpc/dns_server.py
    ```

2. **Start the RPC Server**  
   The RPC server handles client requests. Run it using:

    ```bash
    python Aula_8_RPC/rpc/server.py
    ```

3. **Run the RPC Client**  
   The RPC client sends requests to the server. Test it using:

    ```bash
    python Aula_8_RPC/test_client.py
    ```

4. **Visualize Logs with Streamlit**  
   The Streamlit app provides a dashboard for visualizing logs. Run it using:

    ```bash
    streamlit run Aula_8_RPC/display_logs.py
    ```

## 📝 Usage Examples

### RPC Client
You can use the RPC client to perform operations like:

- **Addition:** `client.sum(10, 20)`
- **Multiplication:** `client.mul(5, 6)`
- **Prime number checking:** `client.check_primes([11, 13, 15])`

### Streamlit Dashboard
The Streamlit app (`display_logs.py`) provides a user-friendly interface to:
- Visualize logs generated by the RPC server.
- Analyze performance metrics (e.g., response times).

![image](https://github.com/user-attachments/assets/cca250d4-ce59-4047-8d7c-cf2f2fc8e2a2)

![image](https://github.com/user-attachments/assets/44625d08-c8bd-4088-9030-55ade8c7e7af)

![image](https://github.com/user-attachments/assets/4992a9bb-c124-4fd5-b997-05c7ef8943d4)

![image](https://github.com/user-attachments/assets/b1104a58-ab62-4051-b850-867955970e06)

![image](https://github.com/user-attachments/assets/e503d1b4-dd5b-4352-88fa-ba6648ba69d9)

![image](https://github.com/user-attachments/assets/46ea1aae-6b4e-404c-a32e-fa1c3071ef3f)

## 🔒 SSL Configuration

The project uses SSL to secure communication between the client and server. The following files are required:
- `cert.pem`: SSL certificate.
- `key.pem`: SSL private key.

These files are located in the `rpc/` folder. If you need to regenerate them, use the following command:

```bash
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes
```

## 📊 Logging

The RPC server generates logs in the following format:

```
timestamp, client_ip, operation, elapsed_time
```

These logs are saved to a file specified in the `config.json` file and can be visualized using the Streamlit app.

## 🛑 Troubleshooting

1. **ModuleNotFoundError**  
   If you encounter a `ModuleNotFoundError`, ensure that all dependencies are installed:

    ```bash
    pip install -r Aula_8_RPC/requirements.txt
    ```

2. **SSL Certificate Issues**  
   If the SSL certificate is not valid for `127.0.0.1`, regenerate it with the correct Common Name (CN) or Subject Alternative Name (SAN):

    ```bash
    openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes -addext "subjectAltName=IP:127.0.0.1"
    ```

3. **Streamlit App Not Working**  
   Ensure that the `requirements.txt` file includes Streamlit and other required dependencies. If deploying on Streamlit Cloud, ensure that `requirements.txt` is in the correct location.

## 📜 License

This project is licensed under the MIT License. See the LICENSE file for details.

## 🙏 Acknowledgments

This project was developed as part of the Distributed Systems course.

Special thanks to the instructors and peers for their guidance and support.

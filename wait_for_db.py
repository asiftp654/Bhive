#!/usr/bin/env python3
"""
Cross-platform database connection wait script.
Works on Linux, macOS, and Windows.
"""
import os
import sys
import time
import socket
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

def wait_for_database(host, port, timeout=60):
    # For running migrations, we need to wait for the database to be available
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        try:
            # Create a socket connection to test if the database is ready
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)  # 1 second timeout for each attempt
            result = sock.connect_ex((host, port))
            sock.close()
            
            if result == 0:
                logger.info(f"Database at {host}:{port} is ready!")
                return True
                
        except socket.gaierror as e:
            logger.debug(f"DNS resolution failed: {e}")
        except Exception as e:
            logger.debug(f"Connection attempt failed: {e}")
        
        logger.info(f"Waiting for database at {host}:{port}...")
        time.sleep(1)
    
    logger.error(f"Timeout reached. Database at {host}:{port} is not available after {timeout} seconds.")
    return False

def main():
    """Main function to handle database wait logic."""
    # Get database connection details from environment variables
    db_host = os.getenv('DB_HOST', 'localhost')
    db_port = int(os.getenv('DB_PORT', '5432'))
    timeout = int(os.getenv('DB_WAIT_TIMEOUT', '60'))
    
    logger.info(f"Waiting for database at {db_host}:{db_port}...")
    
    if wait_for_database(db_host, db_port, timeout):
        logger.info("Database is ready!")
        sys.exit(0)
    else:
        logger.error("Database connection failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()

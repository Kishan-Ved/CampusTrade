import logging
import datetime
import mysql.connector
import os

# Configure file logging
def setup_logger():
    """Set up and configure the logger for both file and console output."""
    # Create logs directory if it doesn't exist
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    # Configure the logger
    logger = logging.getLogger('api_logger')
    logger.setLevel(logging.INFO)
    
    # Create file handler for local logging
    file_handler = logging.FileHandler('logs/api_transactions.log')
    file_handler.setLevel(logging.INFO)
    
    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    # Create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    # Also create a simple audit log file
    audit_handler = logging.FileHandler('logs/auditlog.txt')
    audit_handler.setLevel(logging.INFO)
    audit_formatter = logging.Formatter('%(asctime)s | %(message)s', '%Y-%m-%d %H:%M:%S')
    audit_handler.setFormatter(audit_formatter)
    logger.addHandler(audit_handler)
    
    return logger

# Create a function to log API actions to both file and database
def log_api_action(db_config, action, description, user_id=None):
    """
    Log an API action to both file and database.
    
    Args:
        db_config: Database configuration dictionary
        action: The API action/endpoint being called
        description: Description of the action
        user_id: Optional user ID associated with the action
    """
    # Get the logger
    logger = logging.getLogger('api_logger')
    
    # Log to file
    log_message = f"Action: {action} | Description: {description}"
    if user_id:
        log_message += f" | User: {user_id}"
    
    logger.info(log_message)
    
    # Log to database
    try:
        # Connect to database
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        # Check if api_logs table exists, if not create it
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS api_logs (
                log_id INT AUTO_INCREMENT PRIMARY KEY,
                action VARCHAR(100) NOT NULL,
                description TEXT NOT NULL,
                user_id VARCHAR(50),
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        
        # Insert log entry
        cursor.execute("""
            INSERT INTO api_logs (action, description, user_id)
            VALUES (%s, %s, %s)
        """, (action, description, user_id))
        conn.commit()
        
    except mysql.connector.Error as err:
        logger.error(f"Database error while logging: {err}")
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

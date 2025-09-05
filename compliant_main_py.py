# main.py - FOLLOWS coding standards
import logging
import sys
import os
from typing import Optional
from datetime import datetime
from database import DatabaseConnection
from user_service import UserService


class ApplicationManager:
    """
    Main application orchestrator for user management workflow.
    
    This class coordinates the complete user processing workflow including
    database initialization, user validation, and report generation.
    Provides centralized logging and error handling for the entire application.
    """
    
    def __init__(self):
        self.databaseConnection = DatabaseConnection()
        self.userService = UserService()
        self.minimumAge = int(os.getenv('MINIMUM_USER_AGE', '18'))
        self._setupLogging()
        
    def executeWorkflow(self) -> bool:
        """
        Executes the complete user management workflow.
        
        Returns:
            bool: True if workflow completed successfully, False otherwise
        """
        startTime = datetime.now()
        logging.info("Starting user management workflow")
        
        try:
            if not self._initializeSystem():
                return False
                
            processedUsers = self._processUserData()
            if not processedUsers:
                logging.warning("No users to process")
                return False
                
            self._generateReports(processedUsers)
            self._logWorkflowSummary(startTime, len(processedUsers))
            
            logging.info("Workflow completed successfully")
            return True
            
        except Exception as e:
            logging.error(f"Workflow failed: {e}")
            return False
    
    def _initializeSystem(self) -> bool:
        """
        Initializes database and system components.
        
        Returns:
            bool: True if initialization successful
        """
        logging.info("Initializing system components")
        
        if not self.databaseConnection.initializeDatabase():
            logging.error("Database initialization failed")
            return False
            
        logging.info("System initialization completed")
        return True
    
    def _processUserData(self) -> Optional[list]:
        """
        Processes and validates user data.
        
        Returns:
            Optional[list]: List of processed users or None if processing failed
        """
        logging.info(f"Processing user data with minimum age: {self.minimumAge}")
        
        processedUsers = self.userService.processUsersWithValidation(self.minimumAge)
        
        if processedUsers:
            logging.info(f"Successfully processed {len(processedUsers)} users")
        else:
            logging.warning("No valid users found after processing")
            
        return processedUsers
    
    def _generateReports(self, userList: list) -> None:
        """
        Generates reports from processed user data.
        
        Args:
            userList: List of processed user data
        """
        logging.info("Generating user reports")
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"user_report_{timestamp}.csv"
        
        exportPath = self.userService.exportToCsv(userList, filename)
        logging.info(f"Report generated: {exportPath}")
    
    def _logWorkflowSummary(self, startTime: datetime, userCount: int) -> None:
        """
        Logs workflow execution summary.
        
        Args:
            startTime: Workflow start time
            userCount: Number of processed users
        """
        executionTime = (datetime.now() - startTime).total_seconds()
        
        logging.info("=== Workflow Summary ===")
        logging.info(f"Users processed: {userCount}")
        logging.info(f"Execution time: {executionTime:.2f} seconds")
        logging.info(f"Minimum age filter: {self.minimumAge}")
        logging.info("========================")
    
    def _setupLogging(self) -> None:
        """Configures application logging with appropriate format and level."""
        logLevel = os.getenv('LOG_LEVEL', 'INFO').upper()
        
        logging.basicConfig(
            level=getattr(logging, logLevel),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(sys.stdout),
                logging.FileHandler('app.log', mode='a')
            ]
        )


def main() -> None:
    """
    Main entry point for the user management application.
    
    Initializes the application manager and executes the workflow,
    setting appropriate exit codes based on execution results.
    """
    applicationManager = ApplicationManager()
    
    try:
        success = applicationManager.executeWorkflow()
        exitCode = 0 if success else 1
        
    except KeyboardInterrupt:
        logging.info("Application interrupted by user")
        exitCode = 130
        
    except Exception as e:
        logging.critical(f"Unexpected error: {e}")
        exitCode = 1
    
    sys.exit(exitCode)


if __name__ == "__main__":
    main()
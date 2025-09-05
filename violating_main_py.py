# main.py - VIOLATES coding standards  
import os
import sys
import time
import threading  # unused import
import json  # unused import
from user_service import user_service, report_exporter

# No class documentation
class application_manager:  # snake_case class name
    def __init__(self):
        # Hardcoded secrets (security violation)
        self.app_secret_key = "super_secret_app_key_2024"
        self.database_password = "db_admin_pass_123"
        self.jwt_secret = "jwt_signing_key_xyz789"
        
    def run_full_application_workflow(self, minimum_age):
        # Method exceeds 40 lines (violation)
        print("=" * 50)  # print violation
        print("Starting User Management Application")
        print("=" * 50)
        
        start_time = time.time()
        unused_config = {"debug": True, "verbose": False}  # unused variable
        snake_case_service = user_service()  # naming convention violation
        snake_case_exporter = report_exporter()  # naming convention violation
        temp_results = None  # unused variable
        processing_errors = 0
        
        try:
            print(f"Application started at: {time.strftime('%Y-%m-%d %H:%M:%S')}")
            print("Initializing services...")
            
            print("Step 1: Database connection and setup")
            print("Database connection established")
            
            print("Step 2: User data processing and validation")
            print(f"Applying minimum age filter: {minimum_age}")
            
            validated_users = snake_case_service.process_users_with_validation(minimum_age)
            
            if not validated_users:
                print("ERROR: No valid users found!")
                print("Application cannot continue without valid user data")
                return False
                
            print(f"Successfully processed {len(validated_users)} valid users")
            
            print("Step 3: Generating reports and exports")
            
            # Create output directory if it doesn't exist
            output_path = "/tmp/reports"
            if not os.path.exists(output_path):
                os.makedirs(output_path)
                print(f"Created output directory: {output_path}")
            
            print("Exporting user data to CSV format...")
            snake_case_exporter.export_users_to_csv(validated_users)
            
            print("Step 4: Application summary")
            execution_time = time.time() - start_time
            print(f"Total users processed: {len(validated_users)}")
            print(f"Processing errors: {processing_errors}")
            print(f"Execution time: {execution_time:.2f} seconds")
            
            print("=" * 50)
            print("Application completed successfully!")
            print("=" * 50)
            
            return True
            
        except Exception as e:
            print(f"CRITICAL ERROR: Application failed - {str(e)}")
            print("Check logs for more details")
            return False

def main():
    # snake_case variable naming violation
    app_manager = application_manager()
    minimum_user_age = 18
    
    print("Initializing User Management System...")
    
    success = app_manager.run_full_application_workflow(minimum_user_age)
    
    if success:
        print("System shutdown: SUCCESS")
        exit_code = 0
    else:
        print("System shutdown: FAILURE") 
        exit_code = 1
        
    print(f"Exit code: {exit_code}")  # print violation
    sys.exit(exit_code)

if __name__ == "__main__":
    main()
"""
Background Scheduler for Data Updates
Automatically runs data_updater.py every hour when FastAPI starts
"""

import logging
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from datetime import datetime
import sys
import os

# Add parent directory to path to import data_updater
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

try:
    from data_updater import update_data_files
    UPDATER_AVAILABLE = True
except ImportError:
    UPDATER_AVAILABLE = False
    logging.warning("data_updater.py not found - scheduled updates disabled")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Global scheduler instance
scheduler = None


def run_data_update():
    """
    Job function that runs every hour to update plant data
    """
    try:
        logger.info("🔄 Starting scheduled data update...")
        start_time = datetime.now()
        
        if not UPDATER_AVAILABLE:
            logger.error("❌ data_updater module not available")
            return
        
        # Call the update function
        update_data_files()
        
        elapsed = (datetime.now() - start_time).total_seconds()
        logger.info(f"✅ Data update completed successfully in {elapsed:.2f}s")
        
    except Exception as e:
        logger.error(f"❌ Error during scheduled data update: {str(e)}", exc_info=True)


def start_scheduler():
    """
    Start the background scheduler when FastAPI starts
    """
    global scheduler
    
    if not UPDATER_AVAILABLE:
        logger.warning("⚠️ Scheduler not started - data_updater module not available")
        return None
    
    if scheduler is not None:
        logger.warning("⚠️ Scheduler already running")
        return scheduler
    
    try:
        scheduler = BackgroundScheduler()
        
        # Schedule the job to run every hour
        scheduler.add_job(
            func=run_data_update,
            trigger=IntervalTrigger(hours=1),
            id='data_update_job',
            name='Hourly Plant Data Update',
            replace_existing=True,
            max_instances=1  # Prevent overlapping runs
        )
        
        scheduler.start()
        logger.info("✅ Background scheduler started - data will update every hour")
        logger.info(f"📅 Next run scheduled for: {scheduler.get_jobs()[0].next_run_time}")
        
        # Optionally run once immediately on startup
        # Uncomment the line below if you want data to update when server starts
        # run_data_update()
        
        return scheduler
        
    except Exception as e:
        logger.error(f"❌ Failed to start scheduler: {str(e)}", exc_info=True)
        return None


def stop_scheduler():
    """
    Stop the background scheduler (called when FastAPI shuts down)
    """
    global scheduler
    
    if scheduler is not None:
        scheduler.shutdown()
        logger.info("🛑 Background scheduler stopped")
        scheduler = None


def get_scheduler_status():
    """
    Get the current status of the scheduler
    Returns dict with scheduler info
    """
    if scheduler is None:
        return {
            "running": False,
            "message": "Scheduler not initialized"
        }
    
    jobs = scheduler.get_jobs()
    
    if not jobs:
        return {
            "running": True,
            "message": "No jobs scheduled",
            "jobs": []
        }
    
    job_info = []
    for job in jobs:
        job_info.append({
            "id": job.id,
            "name": job.name,
            "next_run": str(job.next_run_time) if job.next_run_time else None,
            "trigger": str(job.trigger)
        })
    
    return {
        "running": True,
        "message": f"{len(jobs)} job(s) scheduled",
        "jobs": job_info
    }


# For manual testing
if __name__ == "__main__":
    print("Starting scheduler in test mode...")
    print("Press Ctrl+C to stop\n")
    
    start_scheduler()
    
    try:
        # Keep the script running
        import time
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping scheduler...")
        stop_scheduler()
        print("Scheduler stopped.")

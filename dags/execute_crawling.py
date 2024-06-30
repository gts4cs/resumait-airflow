from __future__ import annotations

from logger import setup_logger
from preprocess import csv_to_vectorDB
from scraper import LinkareerCoverLetterScraper
import os
 
if __name__ == "__main__":
    # Define logger and scraper
    log = setup_logger()
    Linkareer_crawler = LinkareerCoverLetterScraper(log=log, background=True)
    
        
    try:
        # Scraping Linkareer cover letter from the website
        Linkareer_crawler.open_website("https://linkareer.com/cover-letter/search")
        Linkareer_crawler.scrape_data()
    except Exception as e:
        # Stop Scraping when driver meets final page of the cover letter.
        log.error(f"An error occurred: {str(e)}")
    finally:
        # Convert & Align data into CSV file to be used for the RAG
        Linkareer_crawler.convert_to_DataFrame()
        Linkareer_crawler.sort_columns_for_RAG()
        Linkareer_crawler.save_to_csv("./data/Linkareer_Cover_Letter_Data.csv")
        Linkareer_crawler.close_browser()

    # Vector DB
    csv_to_vectorDB("./data/Linkareer_Cover_Letter_Data.csv")

import asyncio
import requests
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, CacheMode

# 1. YOUR WEBHOOK URL
WEBHOOK_URL = "http://172.30.164.146:8080/api/v1/webhooks/yw2pQXux4szmDChJrOeMc"

async def main():
    # 2. Define the "Cleaning" rules
    # This tells the crawler: "Only keep the main content and ignore short menu links"
    run_config = CrawlerRunConfig(
        css_selector="main",        # Targets the main article area of most sites
        word_count_threshold=10,    # Discards tiny snippets like "Click here"
        cache_mode=CacheMode.BYPASS # Ensures we get fresh news every time
    )

    print("🚀 Starting the pro-crawler...")
    async with AsyncWebCrawler() as crawler:
        url = "https://www.nbcnews.com/business"
        result = await crawler.arun(url=url, config=run_config)
        
        if result.success:
            print("✅ Clean scrape successful!")
            
            payload = {
                "source": "Crawl4AI_Pro",
                "title": "NBC Business News",
                "url": url,
                "content": result.markdown[:2000] # Send first 2000 chars of CLEAN text
            }
            
            try:
                response = requests.post(WEBHOOK_URL, json=payload)
                if response.status_code == 200:
                    print("💎 Data sent! Check Activepieces now.")
            except Exception as e:
                print(f"❌ Failed to send: {e}")

if __name__ == "__main__":
    asyncio.run(main())
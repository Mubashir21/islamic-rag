import asyncio
from ingestion.pipeline import run_pipeline

if __name__ == "__main__":
    asyncio.run(
        run_pipeline(
            sitemap_url="https://islamqa.info/sitemaps/en/answers/1/sitemap.xml",
            output_file="data/raw/islamqa.jsonl",
            limit=None
        )
    )
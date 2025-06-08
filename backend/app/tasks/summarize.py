from worker.celery_worker import celery_app
import requests
from bs4 import BeautifulSoup
from app.services import db
from bson import ObjectId
from openai import OpenAI
import logging
import os
from dotenv import load_dotenv
from datetime import datetime, timezone
import time
import threading

load_dotenv()

logger = logging.getLogger(__name__)

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENAI_API_KEY")
)

def update_progress(link_id, status, progress, extra_fields=None):
    update = {
        "status": status,
        "progress": progress,
        "updated_at": datetime.now(timezone.utc)
    }
    if status in ("done", "error"):
        update["finished_at"] = datetime.now(timezone.utc)
    if extra_fields:
        update.update(extra_fields)
    db.collection.update_one(
        {"_id": ObjectId(link_id)},
        {"$set": update}
    )

@celery_app.task
def summarize_url(link_id, url, language):
    try:
        update_progress(link_id, "processing", 5)

        response = requests.get(url, timeout=10)

        soup = BeautifulSoup(response.text, "html.parser")
        paragraphs = soup.find_all("p")
        text = " ".join(p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True))

        if len(text) < 100:
            summary = "Not enough text to summarize"
            update_progress(link_id, "done", 100, {
                "summary": summary,
                "error_message": None
            })
            logger.info(f"[DONE] Summary generated for {url[:60]} (too short content).")
            return

        update_progress(link_id, "processing", 20)

        chat_response = None
        exception_raised = None

        def get_chat_response():
            nonlocal chat_response, exception_raised
            try:
                chat_response = client.chat.completions.create(
                    model="deepseek/deepseek-r1-0528:free",
                    messages=[
                        {
                            "role": "user",
                            "content": f"Summarize this article in {language} in max. 5 sentences, provide only the summary as the answer without any unnecessary additions.\n\n{text}"
                        }
                    ],
                    extra_headers={
                        "HTTP-Referer": "http://localhost",
                        "X-Title": "AI Summarizer"
                    }
                )
            except Exception as e:
                exception_raised = e

        thread = threading.Thread(target=get_chat_response)
        thread.start()

        progress = 20
        max_progress = 90
        start_time = time.time()
        estimated_duration = 10 

        while thread.is_alive():
            elapsed = time.time() - start_time
            progress = 20 + (elapsed / estimated_duration) * (max_progress - 20)
            if progress > max_progress:
                progress = max_progress
            update_progress(link_id, "processing", int(progress))
            time.sleep(1)

        thread.join()

        if exception_raised:
            raise exception_raised

        if chat_response is None:
            raise Exception("Brak odpowiedzi od AI")

        summary = chat_response.choices[0].message.content.strip()

        update_progress(link_id, "done", 100, {
            "summary": summary,
            "error_message": None
        })

        logger.info(f"[DONE] Summary generated for {url[:60]}...")

    except Exception as e:
        logger.error(f"[ERROR] summarizing {url}: {e}")
        update_progress(link_id, "error", 100, {
            "summary": None,
            "error_message": str(e)
        })

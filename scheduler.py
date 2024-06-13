from apscheduler.schedulers.background import BackgroundScheduler
from models.google_models import (
    ScrapySitesPlatformAccount,
    database,
)
from filelock import FileLock
from logger import logger
from pathlib import Path

_global_sheduler = None


def init_schduler():
    with FileLock("./scheduler.txt.lock"):
        file = './flag.txt'
        fp = Path(file)
        global _global_sheduler
        if _global_sheduler is None and fp.exists() is False:
            fp.write_text('success', encoding='utf8')
            _global_sheduler = scheduler = BackgroundScheduler()

            def reset_google_account():
                try:
                    logger.info('clear cache')
                    from app import cache
                    cache.clear()
                    logger.info("start reset can use")
                    if database.is_closed():
                        database.connect(reuse_if_open=True)
                    ScrapySitesPlatformAccount.update(can_use=1).execute()
                    logger.info("reset can use success")
                    database.close()
                except:
                    logger.error("reset can use fail", exc_info=True)

            def test():
                logger.info("test task")

            logger.info("init schduler success")

            scheduler.add_job(reset_google_account, "cron", hour=0, minute=1)
            scheduler.add_job(test, "interval", minutes=1)
            scheduler.start()

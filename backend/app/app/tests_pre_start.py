import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

max_tries = 60 * 5  # 5 minutes
wait_seconds = 1


def main() -> None:
    logger.info("Initializing service")
    logger.info("Service finished initializing")


if __name__ == "__main__":
    main()

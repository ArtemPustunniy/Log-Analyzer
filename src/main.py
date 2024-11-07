import logging
import platform
import sys

from src.facades.log_analyzer_facade import LogAnalyzerFacade
from src.parsers.arguments_parser import ArgumentsParser

logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)
logger = logging.getLogger(__name__)


def main(args) -> None:
    logger.info(platform.python_version())
    arguments_parser = ArgumentsParser()
    facade = LogAnalyzerFacade(arguments_parser=arguments_parser, args=args)
    facade.analyze_logs()


if __name__ == "__main__":
    main(args=sys.argv[1:])

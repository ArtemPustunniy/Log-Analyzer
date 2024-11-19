from src.converters.converter import IConverter
from src.services.analytics.analyzer_intrerface import IAnalyzer


class FromNginxLogsToAdocConverter(IConverter):
    """
    Converter class to generate an AsciiDoc report from NGINX log data.

    The `FromNginxLogsToAdocConverter` class inherits from `Converter` and provides a
    method `convert` that transforms analyzed NGINX log data into a structured AsciiDoc
    report, including general metrics, requested resources, and response codes.
    """

    def create_a_report(self, analyzer: IAnalyzer) -> str:
        """
        Converts analyzed NGINX log data to an AsciiDoc report.

        This method uses the data provided by the `analyzer` to construct an AsciiDoc
        document with sections on general metrics, requested resources, and response codes.

        Args:
            analyzer: An object that provides analysis methods for log data, such as
                      start and end dates, request counts, average response size, etc.

        Returns:
            str: An AsciiDoc-formatted string containing the analyzed data report.
        """
        builder = ["= Анализ логов Nginx\n\n", "== Общая информация\n\n", "[cols=\"2,1\", options=\"header\"]\n",
                   "|===\n", "| Метрика | Значение\n", "| Файл(-ы) | access.log\n"]

        start_date = analyzer.get_start_date().strftime("%d.%m.%Y") if analyzer.get_start_date() else "-"
        end_date = analyzer.get_end_date().strftime("%d.%m.%Y") if analyzer.get_end_date() else "-"

        builder.append(f"| Начальная дата | {start_date}\n")
        builder.append(f"| Конечная дата | {end_date}\n")
        builder.append(f"| Количество запросов | {analyzer.get_count_logs()}\n")

        average_size = analyzer.get_average_size_logs()
        builder.append(f"| Средний размер ответа | {average_size:.0f}b\n")

        percentile_95 = analyzer.calculate_95th_percentile()
        builder.append(f"| 95p размера ответа | {percentile_95:.0f}b\n")

        builder.append(f"| Количество уникальных IP | {analyzer.get_unique_ip_count()}\n")
        builder.append(f"| Процент ошибок (4xx и 5xx) | {analyzer.get_error_rate():.2f}%\n")

        builder.append("|===\n\n")

        builder.append("== Запрашиваемые ресурсы\n\n")
        builder.append("[cols=\"2,1\", options=\"header\"]\n")
        builder.append("|===\n")
        builder.append("| Ресурс | Количество\n")

        resource_counts = analyzer.get_requested_resources()
        sorted_resources = sorted(resource_counts.items(), key=lambda item: item[1], reverse=True)
        for resource, count in sorted_resources:
            builder.append(f"| {resource} | {count}\n")

        builder.append("|===\n\n")

        builder.append("== Коды ответа\n\n")
        builder.append("[cols=\"3,2,1\", options=\"header\"]\n")
        builder.append("|===\n")
        builder.append("| Код | Имя | Количество\n")

        status_code_counts = analyzer.get_status_code_counts()
        sorted_status_codes = sorted(status_code_counts.items(), key=lambda item: item[1], reverse=True)
        for code, count in sorted_status_codes:
            code_name = analyzer.get_status_code_name(code)
            builder.append(f"| {code} | {code_name} | {count}\n")

        builder.append("|===\n")

        return "".join(builder)

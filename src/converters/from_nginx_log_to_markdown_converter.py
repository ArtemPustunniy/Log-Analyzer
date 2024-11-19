from src.converters.converter import IConverter
from src.services.analytics.analyzer_intrerface import IAnalyzer


class FromNginxLogToMarkDownConverter(IConverter):
    """
    Converter class to generate a Markdown report from NGINX log data.

    The `FromNginxLogToMarkDownConverter` class inherits from `Converter` and provides a
    method `convert` that transforms analyzed NGINX log data into a structured Markdown
    report, including general metrics, requested resources, and response codes.
    """

    def create_a_report(self, analyzer: IAnalyzer) -> str:
        """
        Converts analyzed NGINX log data to a Markdown report.

        This method uses the data provided by the `analyzer` to construct a Markdown
        document with sections on general metrics, requested resources, and response codes.

        Args:
            analyzer: An object that provides analysis methods for log data, such as
                      start and end dates, request counts, average response size, etc.

        Returns:
            str: A Markdown-formatted string containing the analyzed data report.
        """
        builder = ["#### Общая информация\n\n", "|        Метрика        |     Значение |\n",
                   "|:---------------------:|-------------:|\n", "|       Файл(-ы)        | `access.log` |\n"]

        start_date = analyzer.get_start_date().strftime("%d.%m.%Y") if analyzer.get_start_date() else "-"
        end_date = analyzer.get_end_date().strftime("%d.%m.%Y") if analyzer.get_end_date() else "-"

        builder.append(f"|    Начальная дата     |   {start_date} |\n")
        builder.append(f"|     Конечная дата     |   {end_date} |\n")

        builder.append(
            f"|  Количество запросов  |       {self.format_number_with_underscores(analyzer.get_count_logs())} |\n")

        average_size = analyzer.get_average_size_logs()
        builder.append(f"| Средний размер ответа |         {average_size:.0f}b |\n")

        percentile_95 = analyzer.calculate_95th_percentile()
        builder.append(f"|   95p размера ответа  |         {percentile_95:.0f}b |\n")

        # Additional metrics
        builder.append(
            f"| Количество уникальных IP |        {self.format_number_with_underscores(analyzer.get_unique_ip_count())} |\n")
        builder.append(f"| Процент ошибок (4xx и 5xx) |       {analyzer.get_error_rate():.2f}% |\n\n")

        builder.append("#### Запрашиваемые ресурсы\n\n")
        builder.append("|     Ресурс      | Количество |\n")
        builder.append("|:---------------:|-----------:|\n")

        resource_counts = analyzer.get_requested_resources()
        sorted_resources = sorted(resource_counts.items(), key=lambda item: item[1], reverse=True)
        for resource, count in sorted_resources:
            builder.append(f"|  `{resource}`  |      {self.format_number_with_underscores(count)} |\n")
        builder.append("\n")

        builder.append("#### Коды ответа\n\n")
        builder.append("| Код |          Имя          | Количество |\n")
        builder.append("|:---:|:---------------------:|-----------:|\n")

        status_code_counts = analyzer.get_status_code_counts()
        sorted_status_codes = sorted(status_code_counts.items(), key=lambda item: item[1], reverse=True)
        for code, count in sorted_status_codes:
            code_name = analyzer.get_status_code_name(code)
            builder.append(f"| {code} | {code_name} |       {self.format_number_with_underscores(count)} |\n")

        return "".join(builder)

    @staticmethod
    def format_number_with_underscores(number: int) -> str:
        """
        Formats a number with underscores as 1 thousand separators.

        Args:
            number (int): The number to format.

        Returns:
            str: A string representation of the number with underscores.
        """
        return f"{number:,}".replace(",", "_")

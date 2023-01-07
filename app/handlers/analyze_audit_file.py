import pandas
from watchdog.events import FileSystemEventHandler
from prometheus_client import Counter

import json


class AuditFileModificationHandler(FileSystemEventHandler):
    def __init__(self, audit_file_path):
        self.__audit_file_path = audit_file_path
        self.audit_file_analyzer = AuditFileAnalyzer()
        self.line_offset = 0

    def on_modified(self, event):
        if event.src_path == self.__audit_file_path:
            print(
                f"event type: {event.event_type}  path : {event.src_path}"
            )  # TODO: logging

            df = self.audit_file_analyzer.read_audit_file_to_df(
                self.__audit_file_path, self.line_offset
            )
            if len(df):
                self.audit_file_analyzer.count_metrics_from_df(df)

                self.line_offset = self.audit_file_analyzer.count_lines_in_file(
                    self.__audit_file_path
                )

                print(df)  # TODO: refactor


class AuditFileAnalyzer:
    def __init__(self):
        self.message_type = Counter(
            "message_type", "Responses and requests counter", ["type"]
        )
        self.errors = Counter(
            "errors",
            "Responses and requests errors with paths and descriptions counter",
            ["type", "request_path", "description"],
        )
        self.policies = Counter("policies", "Policies used counter", ["policy"])
        self.remote_addresses = Counter(
            "remote_addresses", "IP used in requests counter", ["remote_address"]
        )

    def read_audit_file_to_df(self, file_path, line_offset):  # TODO: try / except
        df = pandas.DataFrame()

        with open(file_path) as data_file:
            for json_obj in data_file.readlines()[line_offset:]:
                unfilteres_df = pandas.json_normalize(json.loads(json_obj))
                unfilteres_df.drop(
                    unfilteres_df.filter(regex="^(?:response|request).data.*").columns,
                    axis=1,
                    inplace=True,
                )
                df = df.append(unfilteres_df)  # TODO: refactor
        return df

    def count_metrics_from_df(self, df):  # TODO: try / except
        # count responses and requests
        for message_type, amount in (
            df[["type"]].value_counts().to_dict().items()
        ):  # message_type: tuple with the only element
            self.message_type.labels(message_type[0]).inc(amount)

        # count errors
        for _, line in df.query("error.notnull()", engine="python").iterrows():
            self.errors.labels(line["type"], line["request.path"], line["error"]).inc()

        # for error_request_path, amount in (
        #     df.query("error.notnull()", engine="python")["request.path"]
        #     .value_counts()
        #     .to_dict()
        #     .items()
        # ):
        #     self.errors_by_paths.labels(error_request_path).inc(amount)

        # count policies used
        # for policy, amount in df[['auth.token_policies']].value_counts().to_dict().items():
        #     self.policies.labels(policy).inc(amount)

        # count ip addresses from request
        for remote_address, amount in (
            df["request.remote_address"].value_counts().to_dict().items()
        ):
            self.remote_addresses.labels(remote_address).inc(amount)

        # TODO: count request.operation

    def count_lines_in_file(self, file_path):  # TODO: try / except
        with open(file_path) as data_file:
            return len(data_file.readlines())


# import os
# import sys
# if os.path.isdir(logs_path):
#     print(f"{logs_path} is a dir. Parse all files inside it")
#     for dir_name, subdirs, files in os.walk(logs_path):
#         for file_name in files:
#             file_path = os.path.join(logs_path, dir_name, file_name)
#             df.append(json_file_to_df(file_path))
# elif os.path.isfile(logs_path):
#     print(f"{logs_path} is a file. Parse it")
#     df = json_file_to_df(logs_path)
# else:
#     print(f"{logs_path} is not a dir or path. Do not know what to do")
#     sys.exit(1)

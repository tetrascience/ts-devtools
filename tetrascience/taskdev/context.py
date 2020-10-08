import typing as t
import typing_extensions as te
from dataclasses import dataclass, field


FileCategory = te.Literal["IDS", "RAW", "PROCESSED"]
JSONType = t.Union[
    str, int, float, bool, None, t.List["JSONType"], t.Dict[str, "JSONType"]
]


class File(te.TypedDict, total=False):
    type: te.Literal["s3"]
    bucket: str
    fileKey: str
    version: t.Optional[str]


class Options(te.TypedDict, total=False):
    is_stream: t.Optional[bool]


class Result(te.TypedDict):
    metadata: t.Dict[str, str]
    body: bytes
    custom_metadata: t.Dict[str, str]
    custom_tags: t.List[str]


@dataclass
class Context:
    """A development-time version of the context object that is passed into
    the task script handler when running as part of a pipeline."""

    _storage: t.Dict[str, Result] = field(init=False, repr=False, default_factory=dict)

    def read_file(self, file: File, options: Options = {}) -> Result:
        return self._storage[file["fileKey"]]

    def write_file(
        self,
        content: bytes,
        file_name: str,
        file_category: FileCategory,
        ids: str,
        custom_metadata: t.Dict[str, str],
        custom_tags: t.List[str],
        source_type: str,
    ) -> File:
        file: File = {
            "type": "s3",
            "bucket": "fake-unittest-bucket",
            "fileKey": file_name,
        }

        self._storage[(file["bucket"], file["fileKey"])] = {
            "metadata": {"TS_IDS": ids, "TS_SOURCE_TYPE": source_type,},
            "body": content,
            "custom_metadata": custom_metadata,
            "custom_tags": custom_tags,
        }
        return file


def foo(input: File, context: Context):
    context.read_file(input, {"is_stream": True})


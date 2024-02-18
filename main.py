import json
import typing as t
import json as json_module
from dataclasses import dataclass
from abc import ABC, abstractmethod

_JSON_INTERIOR: t.TypeAlias = dict[str, "_JSON_INTERIOR"] | list["_JSON_INTERIOR"] | str | int | float | bool | None
JSON: t.TypeAlias = dict[str, _JSON_INTERIOR]


class BitBucketClient:
    def fail_build(self, org: str) -> None:
        print(f"failing the build :( org: {org}")


class ArtClient:
    ...


class Clients:
    def __init__(self, bit_bucket_client: BitBucketClient, art_client: ArtClient):
        self.bb = bit_bucket_client
        self.art = art_client


class UnknownEventException(Exception):
    ...


@dataclass()
class BitBucketInfo:
    org: str


class Event(ABC):
    bit_bucket_info: BitBucketInfo

    @abstractmethod
    def handle(self, clients: Clients) -> None:
        ...

    @classmethod
    @abstractmethod
    def from_json(cls, json: JSON) -> t.Self:
        ...


def scan_code() -> None:
    ...


def push_to_artifactory() -> None:
    ...


@dataclass()
class PushEvent(Event):
    source: str
    dest: str
    test: str
    bitbucket_info: BitBucketInfo

    def handle(self, clients: Clients) -> None:
        scan_code()
        print("doing something with push events")

    @classmethod
    def from_json(cls, json: JSON) -> t.Self:
        return cls(source="x", dest="y", test="", bitbucket_info=BitBucketInfo(org="x"))


@dataclass()
class MergeEvent(Event):
    source: str
    dest: str
    bitbucket_info: BitBucketInfo

    def handle(self, clients: Clients) -> None:
        scan_code()
        push_to_artifactory()
        print("doing something with merge events")

    @classmethod
    def from_json(cls, json: JSON) -> t.Self:
        return cls(source="x", dest="y", bitbucket_info=BitBucketInfo(org="x"))


def get_event(input_json: JSON) -> Event:
    if "push" in input_json:
        return PushEvent.from_json(input_json)
    elif "merge" in input_json:
        return MergeEvent.from_json(input_json)
    else:
        raise UnknownEventException(f"Could not get type from input json:\n{json.dumps(input_json, indent=4)}")


def parse_input(input_str: str) -> JSON:
    result = json_module.loads(input_str)
    if type(result) == dict:
        return result
    else:
        raise ValueError(f"input_str was not of type dict:\n{input_str}")


def main() -> None:
    clients = Clients(art_client=ArtClient(), bit_bucket_client=BitBucketClient())
    input_str = '{"p": 1}'
    try:
        input_json = parse_input(input_str=input_str)
        event = get_event(input_json)
        event.handle(clients)
    except Exception:
        clients.bb.fail_build("ad")
        raise


if __name__ == "__main__":
    main()

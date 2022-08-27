#!/usr/bin/env python3

"""
DEAR ANYONE READING THIS REPO:
this script is worthless, i smoothbrained comparing the two logs visually, smh
"""

import dataclasses
from datetime import datetime, timedelta
from dateutil.parser import parse
from typing import List
    
DELTA = timedelta(seconds=10)

def within(ts1: datetime, ts2: datetime) -> bool:
    return ts1-DELTA <= ts2 and ts2 <= ts1 + DELTA 

@dataclasses.dataclass
class Entry:
    ts: datetime
    hacker: str
    client_id: int
    payment: float

    @staticmethod
    def from_csv_row(row):
        parts = row.split(",")
        return Entry(parse(parts[0]), parts[1], int(parts[2]), float(parts[3]))
    
    def __str__(self):
        return ",".join((self.ts.strftime("%Y-%m-%dT%H:%M:%S%z"),
                         self.hacker,
                         str(self.client_id),
                         str(self.payment)))
    
    def __hash__(self):
        return (self.hacker, self.client_id, self.payment).__hash__()

    def __eq__(self, other):
        return (isinstance(other, self.__class__) and
        within(self.ts, other.ts) and
        other.hacker == self.hacker and
        other.client_id == self.client_id and
        other.payment == self.payment)

def main():
    log_entries: List[Entry] = []
    db_entries: List[Entry] = []

    unmatched: List[Entry] = []

    with open("log_rows.csv", "r") as f:
        for x in f.readlines():
            log_entries.append(Entry.from_csv_row(x.strip()))
    with open("db_rows.csv", "r") as f:
        for x in f.readlines():
            db_entries.append(Entry.from_csv_row(x.strip()))

    """
    delta = timedelta(seconds=10)
    for log_entry in log_entries:
        # find a db entry within 10sec of the log entry
        # this can be O(n^2) b/c small dataset and i am lazy

        found = False
        for db_entry in db_entries:
            if db_entry.ts - delta <= log_entry.ts <= db_entry.ts + delta:
                found = True
                break
        
        if not found:
            unmatched.append(log_entry)
    """

    unmatched.extend(db_entries)
    for x in log_entries:
        if x in unmatched:
            unmatched.remove(x)
    
    print(len(unmatched))
    print("\n".join([str(x) for x in unmatched]))

if __name__ == "__main__":
    main()
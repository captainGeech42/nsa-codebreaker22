#!/usr/bin/env python3

import sys

from datetime import datetime, timedelta
from typing import Dict, List

# Node,Username,Start Time,Duration,Service,Active,Auth,Real Ip,Vpn Ip,Proto,Port,Bytes Total,Error
class Record:
    def __init__(self, row: str):
        parts = row.split(",")
        assert len(parts) == 13

        try:
            self.node = parts[0]
            self.username = parts[1]
            self.start_time = datetime.strptime(parts[2][:-4], "%Y.%m.%d %H:%M:%S") if len(parts[2]) > 0 else None # 2022.05.20 17:29:12 EDT
            self.duration = timedelta(seconds=float(parts[3])) if len(parts[3]) > 0 else None
            self.service = parts[4]
            self.active = parts[5] == "1"
            self.auth = parts[6] == "1"
            self.real_ip = parts[7]
            self.vpn_ip = parts[8]
            self.proto = parts[9]
            self.port = int(parts[10]) if len(parts[10]) > 0 else None
            self.bytes_total = int(parts[11]) if len(parts[11]) > 0 else None
            self.error = parts[12]
        except:
            print(f"failed to parse row: {row}")
    
    def __hash__(self) -> int:
        return hash((self.start_time, self.username))

def get_records(fp: str) -> List[Record]:
    with open(fp, "r") as f:
        f.readline()

        return [Record(x) for x in f.readlines()]

def find_overlapping_session(records: List[Record]) -> List[str]:
    """Find usernames who had overlapping sessions"""

    # build map of username->Record
    user_rec_map: Dict[str, List[Record]] = {}

    for r in records:
        # only do authenticated sessions
        if r.auth:
            if r.username not in user_rec_map.keys():
                user_rec_map[r.username] = []
        
            user_rec_map[r.username].append(r)

    flagged = []
    
    # check each user's logins
    for user in user_rec_map.keys():
        # can't be overlapping sessions if there is only one
        if len(user_rec_map[user]) < 2:
            continue
        
        for i in range(1, len(user_rec_map[user])):
            if user_rec_map[user][i].start_time < user_rec_map[user][i-1].start_time + user_rec_map[user][i-1].duration:
                flagged.append(user)
    
    return flagged

def main() -> int:
    records = get_records("./vpn.log")

    print(find_overlapping_session(records))
    return 0

if __name__ == "__main__":
    sys.exit(main())
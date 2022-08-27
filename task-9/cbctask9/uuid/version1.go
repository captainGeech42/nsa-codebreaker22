// Copyright 2016 Google Inc.  All rights reserved.
// Use of this source code is governed by a BSD-style
// license that can be found in the LICENSE file.

package uuid

import (
	"encoding/binary"
	"time"
)

// NewUUID returns a Version 1 UUID based on the current NodeID and clock
// sequence, and the current time.  If the NodeID has not been set by SetNodeID
// or SetNodeInterface then it will be set automatically.  If the NodeID cannot
// be set NewUUID returns nil.  If clock sequence has not been set by
// SetClockSequence then it will be set automatically.  If GetTime fails to
// return the current NewUUID returns nil and an error.
//
// In most cases, New should be used.
func NewUUID(ts time.Time) (UUID, error) {
	var uuid UUID
	now, _, err := GetTime(ts)
	if err != nil {
		return uuid, err
	}

	timeLow := uint32(now & 0xffffffff)
	// fmt.Printf("low: %x\n", timeLow)
	timeMid := uint16((now >> 32) & 0xffff)
	// fmt.Printf("mid: %x\n", timeMid)
	timeHi := uint16((now >> 48) & 0x0fff)
	timeHi |= 0x1000 // Version 1
	// fmt.Printf("hi: %x\n", timeHi)

	// fmt.Printf("seq: %x\n", seq)

	binary.BigEndian.PutUint32(uuid[0:], timeLow)
	binary.BigEndian.PutUint16(uuid[4:], timeMid)
	binary.BigEndian.PutUint16(uuid[6:], timeHi)
	copy(uuid[8:], []byte{0x97, 0x4f})

	SetNodeID([]byte{0x33, 0x02, 0xa1, 0x51, 0x00, 0x00}) // chal
	// SetNodeID([]byte{0x48, 0x2a, 0xe3, 0x28, 0x00, 0x00}) // test
	copy(uuid[10:], nodeID[:])

	return uuid, nil
}

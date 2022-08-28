package main

import (
	"fmt"
	"os"
	"time"

	"cbctask9/uuid"
)

func main() {
	// fmt.Println("generating uuid for", os.Args[1])

	tm, err := time.Parse("2006-01-02T15:04:05-0700", os.Args[1])
	if err != nil {
		fmt.Println(err)
		os.Exit(1)
	}

	// fmt.Println(tm)

	id, err := uuid.NewUUID(tm)
	if err != nil {
		fmt.Println(err)
	}

	fmt.Println(id.String())
}

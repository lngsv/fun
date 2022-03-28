package main

import (
	"flag"
)

var (
	dsnPtr    *string
	dryPtr    *bool
	limitPtr  *int
	offsetPtr *int
)

func init() {
	limitPtr = flag.Int("limit", 0, "how much to upload")

	offsetPtr = flag.Int("offset", 0, "how much entries to skip")
}

func main()  {
	flag.Parse()
    print(*limitPtr, *offsetPtr)
}

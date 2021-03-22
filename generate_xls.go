package main

import (
	"fmt"
	"github.com/360EntSecGroup-Skylar/excelize"
)

func main() {
	f := excelize.NewFile()
	f.SetSheetRow("Sheet1", "A1", &[]string{"col1", "col2"})
	f.SetSheetRow("Sheet1", "A2", &[]interface{}{"15", 123.5})
	err := f.SaveAs("mytable.xls")
	if err != nil {
		fmt.Println("cannot save", err)
	}
}

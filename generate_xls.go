package main

import (
	"fmt"
	"github.com/360EntSecGroup-Skylar/excelize"
    "strconv"
)

func main() {
	f := excelize.NewFile()
	f.AddTable("Sheet1", "A1", "B1", ``)
	style, err := f.NewStyle(`{"font": {"bold":true}}`)
	if err != nil {
		fmt.Println("error new style", err)
	}
	f.SetSheetRow("Sheet1", "A1", &[]string{"col1", "col2"})
	f.SetCellStyle("Sheet1", "A1", "B1", style)
    rows := [][]interface{}{{"15", 123.5}, {true, 55}}
    for i, row := range rows {
		f.SetSheetRow("Sheet1", "A"+strconv.Itoa(i+2), &row)
	}
	err = f.SaveAs("mytable.xls")
	if err != nil {
		fmt.Println("cannot save", err)
	}
}
package main
import (
    "github.com/jung-kurt/gofpdf"
)

func main() {
    pdf := gofpdf.New("P", "mm", "A4", "")
	pdf.AddPage()
	pdf.AddUTF8Font("dejavu", "", path.Join(getFontsDir(), "DejaVuSansCondensed.ttf"))
	pdf.SetFont("dejavu", "", 14)
	pdf.MultiCell(180, 10, applicationText, "", "", false)

	pdf.OutputFileAndClose()
}

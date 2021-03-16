package main

import (
	"fmt"
	"golang.org/x/text/language"
	"golang.org/x/text/message"
	"golang.org/x/text/number"
	"math"
)

func main() {
	for _, p := range([]float64{1234.015, 1234.016, 1234.5, 1234.0, 1234.6, 1234.012, 24, 1.996}) {
		fmt.Printf("%10.3f : %10s\n", p, formatPrice(p))
	}
}

func formatPrice(price float64) string {
	rounded := math.Round(price * 100) / 100
	withoutFractional := float64(int(rounded))

	p := message.NewPrinter(language.Russian)
	if withoutFractional == rounded {
		return p.Sprint(number.Decimal(withoutFractional)) + " ₽"
	}
	return p.Sprint(number.Decimal(rounded, number.IncrementString("0.01"))) + " ₽"
}
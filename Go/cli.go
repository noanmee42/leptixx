// Go/cli.go

package main

import (
	"fmt"
	"strings"

	"github.com/lucasb-eyer/go-colorful"
	"github.com/muesli/termenv"
)

const asciiLogo = `
██      ███████ ██████  ████████ ██ ██   ██ ██   ██ 
██      ██      ██   ██    ██    ██  ██ ██   ██ ██  
██      █████   ██████     ██    ██   ███     ███  
██      ██      ██         ██    ██  ██ ██   ██ ██ 
███████ ███████ ██         ██    ██ ██   ██ ██   ██ `

func printGradientLogo() {
	p := termenv.ColorProfile()
	lines := strings.Split(asciiLogo, "\n")

	startColor, _ := colorful.Hex("#00BFFF")
	endColor, _ := colorful.Hex("#00008B")

	for i, line := range lines {
		ratio := float64(i) / float64(len(lines))
		resColor := startColor.BlendLuv(endColor, ratio).Hex()
		fmt.Println(termenv.String(line).Foreground(p.Color(resColor)))
	}
	fmt.Println(termenv.String("   CLI App for detecting AI hallucinations.").Italic().Foreground(p.Color("#808080")))
	fmt.Println()
}

func printResults(claimsData ClaimsData, results []FactCheckResult) {
	p := termenv.ColorProfile()
	colorHeader := p.Color("#00BFFF")
	colorOk := p.Color("#3FB950")
	colorErr := p.Color("#FF6B6B")
	colorWarn := p.Color("#D29922")
	colorDim := p.Color("#8B949E")
	colorText := p.Color("#E6EDF3")

	fmt.Println()
	fmt.Println(termenv.String("--------------------------------------------").Foreground(colorHeader))
	fmt.Println(termenv.String("            РЕЗУЛЬТАТЫ ПРОВЕРКИ             ").Foreground(colorText))
	fmt.Println(termenv.String("--------------------------------------------").Foreground(colorHeader))

	fmt.Printf("\n  💬 Ответ: %s\n", claimsData.Response)
	fmt.Println(termenv.String("\n ").Foreground(colorDim))

	for i, result := range results {
		fmt.Printf("\n  [%d] %s\n", i+1, result.Claim)

		if result.Found && result.Result {
			fmt.Println(termenv.String(fmt.Sprintf("      ✅ ФАКТ ПОДТВЕРЖДЁН (достоверность: %.0f%%)", result.Factuality*100)).Foreground(colorOk))
		} else if result.Found && !result.Result {
			fmt.Println(termenv.String(fmt.Sprintf("      ❌ ГАЛЛЮЦИНАЦИЯ (достоверность: %.0f%%)", result.Factuality*100)).Foreground(colorErr))
		} else {
			fmt.Println(termenv.String("      ⚠️  Не удалось проверить").Foreground(colorWarn))
		}

		if result.Reason != "" {
			fmt.Printf("      💬 %s\n", result.Reason)
		}
		if result.ReviewURL != "" {
			fmt.Println(termenv.String(fmt.Sprintf("      🔗 %s", result.ReviewURL)).Foreground(colorDim))
		}
		if result.KeyQuote != "" {
			fmt.Println(termenv.String(fmt.Sprintf("      📝 \"%s\"", result.KeyQuote)).Foreground(colorDim))
		}
	}

	summary := BuildSummary(results)

	fmt.Println()
	fmt.Println(termenv.String("--------------------------------------------").Foreground(colorHeader))
	fmt.Println(termenv.String("                   ВЫВОДЫ                   ").Foreground(colorText))
	fmt.Println(termenv.String("--------------------------------------------").Foreground(colorHeader))
	fmt.Printf("  📊 Всего утверждений:      %d\n", summary.TotalClaims)
	fmt.Println(termenv.String(fmt.Sprintf("  ✅ Подтверждено:            %d", summary.ClaimsFound)).Foreground(colorOk))
	fmt.Println(termenv.String(fmt.Sprintf("  ❌ Не подтверждено:         %d", summary.ClaimsNotFound)).Foreground(colorErr))

	if summary.TotalClaims > 0 {
		pct := float64(summary.PotentialHallucinations) / float64(summary.TotalClaims) * 100
		fmt.Println(termenv.String(fmt.Sprintf("  ⚠️  Возможных галлюцинаций: %d (%.1f%%)", summary.PotentialHallucinations, pct)).Foreground(colorWarn))
	}

	fmt.Println(termenv.String("-----------------------------------------").Foreground(colorHeader))
}

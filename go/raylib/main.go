package main

import (
	"fmt"

	gui "github.com/gen2brain/raylib-go/raygui"

	rl "github.com/gen2brain/raylib-go/raylib"
)

func main() {
	rl.InitWindow(800, 350, "Raylib Test")

	rl.SetTargetFPS(60)

	var button bool
	var counter int64

	for !rl.WindowShouldClose() {
		rl.BeginDrawing()
		rl.ClearBackground(rl.Beige)

		rl.DrawText(fmt.Sprintf("counter: %v", counter), 50, 50, 20, rl.Black)

		button = gui.Button(rl.NewRectangle(50, 150, 100, 40), "Plus")
		if button {
			counter++
		}
		rl.EndDrawing()
	}
	rl.CloseWindow()
}

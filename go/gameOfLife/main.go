/**
 * [X] 1. 2d array: 1 alive 0 dead
 * [X] 2. count neighbors func (grid, row, col) -> number
 * [X] 3. nextState:
 * 	- alive + 2 or 3 = alive
 *  - dead + 3 = alive
 * 	- else = dead
 * [-] 4. step(grid) create new grid
 * [X] 5. print(grid)
 * [X] 6. game loop
 */
package main

import (
	"fmt"
)

const (
	ALIVE = 1
	DEAD  = 0
	COLS  = 3
	ROWS  = 3
)

func main() {
	var grid [][]int
	grid = [][]int{
		{0, 1, 0},
		{0, 1, 0},
		{0, 1, 0},
	}

	for _ = range 5 {
		print(grid)
		grid = nextState(grid)
	}
}

func print(grid [][]int) {
	for i := range len(grid) {
		fmt.Println(grid[i])
	}
	fmt.Println("----------------------")
}

func countNeighbors(grid [][]int, row, col int) int {
	count := 0
	d := [3]int{-1, 0, 1}
	for _, dr := range d {
		for _, dc := range d {
			r := row + dr
			c := col + dc

			if r == row && c == col {
				continue
			}

			if r < 0 || r >= ROWS {
				continue
			}
			if c < 0 || c >= COLS {
				continue
			}
			if grid[r][c] == ALIVE {
				count++
			}
		}
	}
	return count
}

func nextState(grid [][]int) [][]int {
	newGrid := make([][]int, len(grid))
	for r := range grid {
		newGrid[r] = make([]int, len(grid[r]))
		for c := range grid[r] {
			n := countNeighbors(grid, r, c)
			if grid[r][c] == ALIVE {
				if n == 2 || n == 3 {
					newGrid[r][c] = ALIVE
				} else {
					newGrid[r][c] = DEAD
				}
			} else {
				if n == 3 {
					newGrid[r][c] = ALIVE
				} else {
					newGrid[r][c] = DEAD
				}
			}
		}
	}
	return newGrid
}

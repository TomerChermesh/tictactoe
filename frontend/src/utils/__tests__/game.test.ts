import { describe, it, expect } from 'vitest'
import { toSymbol, resolveStartingPlayer, createEmptyBoard } from '../game'
import type { CellValue, SymbolValue } from '../../types/game'
import type { PlayerID } from '../../types/players'


describe('toSymbol', () => {
  it.each<[CellValue, SymbolValue]>([
    [0, null],
    [1, 'X'],
    [2, 'O'],
  ])('should convert %d to %s', (value: CellValue, expected: SymbolValue) => {
    const result: SymbolValue = toSymbol(value)
    expect(result).toBe(expected)
  })
})


describe('resolveStartingPlayer', () => {
  it.each<[CellValue, PlayerID]>([
    [1, 1],
    [2, 2],
  ])('should return %d when choice is %d', (choice: CellValue, expected: PlayerID) => {
    const result: PlayerID = resolveStartingPlayer(choice)
    expect(result).toBe(expected)
  })

  it('should return random player when choice is 0', () => {
    const results: Set<PlayerID> = new Set()
    const iterations: number = 100
    
    for (let i = 0; i < iterations; i++) {
      const result: PlayerID = resolveStartingPlayer(0)
      results.add(result)
      expect([1, 2]).toContain(result)
    }
    
    expect(results.size).toBeGreaterThan(1)
  })
})


describe('createEmptyBoard', () => {
  it('should create board with 9 zeros', () => {
    const result: CellValue[] = createEmptyBoard()
    expect(result).toHaveLength(9)
    expect(result.every(cell => cell === 0)).toBe(true)
  })

  it('should return new array each time', () => {
    const board1: CellValue[] = createEmptyBoard()
    const board2: CellValue[] = createEmptyBoard()
    expect(board1).not.toBe(board2)
    expect(board1).toEqual(board2)
  })
})


import type { CellValue, SymbolValue } from '../types/game'
import { ValueSymbol } from '../types/game'
import type { PlayerID } from '../types/players'

export const toSymbol = (value: CellValue): SymbolValue => {
    if (value === 0) return null
    return ValueSymbol[value] ?? null
  }

export const resolveStartingPlayer = (choice: CellValue): PlayerID =>
    choice === 0
        ? (Math.random() < 0.5 ? 1 : 2)
        : choice

export const createEmptyBoard = (): CellValue[] =>
          Array(9).fill(0) as CellValue[]
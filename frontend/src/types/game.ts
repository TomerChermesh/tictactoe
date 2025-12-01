import type { PlayerID } from './players'

export const ValueSymbol = {
    1: 'X',
    2: 'O'
} as const

export type CellValue = 0 | PlayerID
export type CellIndex = 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8

export type SymbolValue = null | 'X' | 'O'

export interface Game {
    id: string
    matchupId: string
    createdAt: string
    updatedAt: string
    board: CellValue[]
    winner: PlayerID | null
    isFinished: boolean
    currentTurn: PlayerID
    winningTriplet: CellIndex[] | null
}
  
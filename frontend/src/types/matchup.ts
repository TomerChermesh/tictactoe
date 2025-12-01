import type { Game } from './game'
import type { Player } from './players'

export type MatchupMode = 'friend' | 'ai'

export interface Matchup {
    id: string
    userId: string
    mode: MatchupMode
    player1: Player
    player2: Player
    createdAt: string
    updatedAt: string
  }

export interface UpdateResponse {
    matchup: Matchup | null
    game: Game | null
}
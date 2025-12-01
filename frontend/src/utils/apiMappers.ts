import type { Matchup, UpdateResponse } from '../types/matchup'
import type { Game } from '../types/game'

export const normalizeResponse = (response: any): UpdateResponse => ({
    game: response.game ? normalizeGame(response.game) : null,
    matchup: response.matchup ? normalizeMatchup(response.matchup) : null
  })
  
const normalizeGame = (g: any): Game => ({
    id: g.id ?? g._id,
    matchupId: g.matchup_id,
    board: g.board,
    currentTurn: g.current_turn,
    isFinished: g.is_finished,
    winner: g.winner,
    winningTriplet: g.winning_triplet,
    createdAt: g.created_at,
    updatedAt: g.updated_at
  })

const normalizeMatchup = (m: any): Matchup => ({
    id: m.id ?? m._id,
    userId: m.user_id,
    mode: m.mode,
    player1: {id: 1, name: m.player1_name, score: m.player1_score},
    player2: {id: 2, name: m.player2_name, score: m.player2_score},
    createdAt: m.created_at,
    updatedAt: m.updated_at
})

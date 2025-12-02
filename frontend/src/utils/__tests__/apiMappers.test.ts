import { describe, it, expect } from 'vitest'
import { normalizeResponse, normalizeGame, normalizeMatchup } from '../apiMappers'
import type { UpdateResponse, Matchup } from '../../types/matchup'
import type { Game } from '../../types/game'


describe('normalizeGame', () => {
  it.each<[any, Game]>([
    [
      {
        id: 'game123',
        matchup_id: 'matchup123',
        board: [0, 1, 2, 0, 0, 0, 0, 0, 0],
        current_turn: 1,
        is_finished: false,
        winner: null,
        winning_triplet: null,
        created_at: '2024-01-01T00:00:00Z',
        updated_at: '2024-01-01T00:00:00Z'
      },
      {
        id: 'game123',
        matchupId: 'matchup123',
        board: [0, 1, 2, 0, 0, 0, 0, 0, 0],
        currentTurn: 1,
        isFinished: false,
        winner: null,
        winningTriplet: null,
        createdAt: '2024-01-01T00:00:00Z',
        updatedAt: '2024-01-01T00:00:00Z'
      }
    ],
    [
      {
        _id: 'game456',
        matchup_id: 'matchup456',
        board: [1, 1, 1, 2, 2, 0, 0, 0, 0],
        current_turn: 2,
        is_finished: true,
        winner: 1,
        winning_triplet: [0, 1, 2],
        created_at: '2024-01-02T00:00:00Z',
        updated_at: '2024-01-02T00:00:00Z'
      },
      {
        id: 'game456',
        matchupId: 'matchup456',
        board: [1, 1, 1, 2, 2, 0, 0, 0, 0],
        currentTurn: 2,
        isFinished: true,
        winner: 1,
        winningTriplet: [0, 1, 2],
        createdAt: '2024-01-02T00:00:00Z',
        updatedAt: '2024-01-02T00:00:00Z'
      }
    ],
  ])('should normalize game with id field', (input: any, expected: Game) => {
    const result: Game = normalizeGame(input)
    expect(result).toEqual(expected)
  })
})


describe('normalizeMatchup', () => {
  it.each<[any, Matchup]>([
    [
      {
        id: 'matchup123',
        user_id: 'user123',
        mode: 'friend',
        player1_name: 'Player 1',
        player1_score: 5,
        player2_name: 'Player 2',
        player2_score: 3,
        created_at: '2024-01-01T00:00:00Z',
        updated_at: '2024-01-01T00:00:00Z'
      },
      {
        id: 'matchup123',
        userId: 'user123',
        mode: 'friend',
        player1: { id: 1, name: 'Player 1', score: 5 },
        player2: { id: 2, name: 'Player 2', score: 3 },
        createdAt: '2024-01-01T00:00:00Z',
        updatedAt: '2024-01-01T00:00:00Z'
      }
    ],
    [
      {
        _id: 'matchup456',
        user_id: 'user456',
        mode: 'ai',
        player1_name: 'Human',
        player1_score: 2,
        player2_name: 'AI Agent',
        player2_score: 1,
        created_at: '2024-01-02T00:00:00Z',
        updated_at: '2024-01-02T00:00:00Z'
      },
      {
        id: 'matchup456',
        userId: 'user456',
        mode: 'ai',
        player1: { id: 1, name: 'Human', score: 2 },
        player2: { id: 2, name: 'AI Agent', score: 1 },
        createdAt: '2024-01-02T00:00:00Z',
        updatedAt: '2024-01-02T00:00:00Z'
      }
    ],
  ])('should normalize matchup', (input: any, expected: Matchup) => {
    const result: Matchup = normalizeMatchup(input)
    expect(result).toEqual(expected)
  })
})


describe('normalizeResponse', () => {
  it.each<[any, UpdateResponse]>([
    [
      {
        game: {
          id: 'game123',
          matchup_id: 'matchup123',
          board: [0, 0, 0, 0, 0, 0, 0, 0, 0],
          current_turn: 1,
          is_finished: false,
          winner: null,
          winning_triplet: null,
          created_at: '2024-01-01T00:00:00Z',
          updated_at: '2024-01-01T00:00:00Z'
        },
        matchup: {
          id: 'matchup123',
          user_id: 'user123',
          mode: 'friend',
          player1_name: 'Player 1',
          player1_score: 0,
          player2_name: 'Player 2',
          player2_score: 0,
          created_at: '2024-01-01T00:00:00Z',
          updated_at: '2024-01-01T00:00:00Z'
        }
      },
      {
        game: {
          id: 'game123',
          matchupId: 'matchup123',
          board: [0, 0, 0, 0, 0, 0, 0, 0, 0],
          currentTurn: 1,
          isFinished: false,
          winner: null,
          winningTriplet: null,
          createdAt: '2024-01-01T00:00:00Z',
          updatedAt: '2024-01-01T00:00:00Z'
        },
        matchup: {
          id: 'matchup123',
          userId: 'user123',
          mode: 'friend',
          player1: { id: 1, name: 'Player 1', score: 0 },
          player2: { id: 2, name: 'Player 2', score: 0 },
          createdAt: '2024-01-01T00:00:00Z',
          updatedAt: '2024-01-01T00:00:00Z'
        }
      }
    ],
    [
      {
        game: null,
        matchup: null
      },
      {
        game: null,
        matchup: null
      }
    ],
    [
      {
        game: {
          id: 'game789',
          matchup_id: 'matchup789',
          board: [1, 1, 1, 2, 2, 0, 0, 0, 0],
          current_turn: 2,
          is_finished: true,
          winner: 1,
          winning_triplet: [0, 1, 2],
          created_at: '2024-01-03T00:00:00Z',
          updated_at: '2024-01-03T00:00:00Z'
        },
        matchup: null
      },
      {
        game: {
          id: 'game789',
          matchupId: 'matchup789',
          board: [1, 1, 1, 2, 2, 0, 0, 0, 0],
          currentTurn: 2,
          isFinished: true,
          winner: 1,
          winningTriplet: [0, 1, 2],
          createdAt: '2024-01-03T00:00:00Z',
          updatedAt: '2024-01-03T00:00:00Z'
        },
        matchup: null
      }
    ],
  ])('should normalize response', (input: any, expected: UpdateResponse) => {
    const result: UpdateResponse = normalizeResponse(input)
    expect(result).toEqual(expected)
  })
})


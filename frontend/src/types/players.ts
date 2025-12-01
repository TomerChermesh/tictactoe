export type PlayerID = 1 | 2

export interface Player {
  id: PlayerID
  name: string
  score: number
}
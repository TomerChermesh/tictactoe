import React, { useState } from 'react'
import { useGetMatchupsListQuery } from '../api/matchupApi'
import { useLazyGetLastGameForMatchupQuery } from '../api/gameApi'
import { Box, Typography, IconButton, type SvgIconProps } from '@mui/material'
import { DataGrid, type GridColDef } from '@mui/x-data-grid'
import type { Matchup } from '../types/matchup'
import { DATE_TIME_FORMAT, DATE_TIME_FORMAT_OPTIONS } from '../constants/dateTime'
import PeopleIcon from '@mui/icons-material/People'
import SmartToyIcon from '@mui/icons-material/SmartToy'
import ReplayIcon from '@mui/icons-material/Replay'
import { useAppDispatch } from '../store/hooks'
import { setGame } from '../store/gameSlice'
import { useNavigate } from 'react-router-dom'
import type { Game } from '../types/game'
import SnackbarAlert from '../components/general/SnackBarAlert'
import { setMatchup } from '../store/matchupSlice'

const MatchupsListPage: React.FC = () => {
  const { data: matchupsList, isLoading, error } = useGetMatchupsListQuery()
  const [loadLastGame] = useLazyGetLastGameForMatchupQuery()
  const dispatch = useAppDispatch()
  const navigate = useNavigate()

  const [reloadError, setReloadError] = useState<string | null>(null)


  const handleReloadMatchup = async (matchup: Matchup) => {
    try {
      dispatch(setMatchup(matchup))
      const game: Game = await loadLastGame(matchup.id).unwrap()
      console.log('game', game)
      if (game) {
        dispatch(setGame(game))
        navigate('/game')
      } else {
        setReloadError('No game found for this matchup')
      }
    } catch (err: any) {
      setReloadError(`Failed to reload matchup: ${err.data.detail}`)
    }
  }

  const columns: GridColDef<Matchup>[] = [
    {
      field: 'mode',
      headerName: 'Mode',
      width: 120,
      align: 'center',
      headerAlign: 'center',
      renderCell: params => {
        const isFriend: boolean = params.value === 'friend'
        const IconComponent: React.FC<SvgIconProps> = isFriend ? PeopleIcon : SmartToyIcon

        return (
          <Box sx={{ width: '100%', height: '100%', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
            <IconComponent />
          </Box>
        )
      }
    },
    {
      field: 'updatedAt',
      headerName: 'Last Updated',
      width: 180,
      valueGetter: (_value, row) => {
        return new Intl.DateTimeFormat(DATE_TIME_FORMAT, DATE_TIME_FORMAT_OPTIONS).format(new Date(row.updatedAt))
      },
      align: 'center',
      headerAlign: 'center'
    },
    {
      field: 'player1',
      headerName: 'X',
      width: 150,
      align: 'center',
      headerAlign: 'center',
      valueGetter: (_value, row) => row.player1.name,
      renderCell: (params) => (
        <Box sx={{ color: 'warning.main' }}>{params.value}</Box>
      )
    },
    {
      field: 'player1Score',
      headerName: 'P1 Score',
      width: 100,
      align: 'center',
      headerAlign: 'center',
      valueGetter: (_value, row) => row.player1.score,
      renderCell: (params) => (
        <Box sx={{ fontSize: '1.4rem', fontFamily: 'Digital-7' }}>{params.value}</Box>
      )
    },
    {
      field: 'player2',
      headerName: 'O',
      width: 150,
      align: 'center',
      headerAlign: 'center',
      valueGetter: (_value, row) => row.player2.name,
      renderCell: (params) => (
        <Box sx={{ color: 'primary.main' }}>{params.value}</Box>
      )
    },
    {
      field: 'player2Score',
      headerName: 'P2 Score',
      width: 100,
      align: 'center',
      headerAlign: 'center',
      valueGetter: (_value, row) => row.player2.score,
      renderCell: (params) => (
        <Box sx={{ fontSize: '1.4rem', fontFamily: 'Digital-7' }}>{params.value}</Box>
      )
    },
    {
      field: 'createdAt',
      headerName: 'Time Created',
      width: 180,
      align: 'center',
      headerAlign: 'center',
      valueGetter: (_value, row) => {
        return new Intl.DateTimeFormat(DATE_TIME_FORMAT, DATE_TIME_FORMAT_OPTIONS).format(new Date(row.createdAt))
      }
    },
    {
      field: 'reload',
      headerName: 'Reload Matchup',
      width: 180,
      align: 'center',
      headerAlign: 'center',
      sortable: false,
      filterable: false,
      renderCell: params => (
        <IconButton onClick={() => handleReloadMatchup(params.row)} aria-label='reload matchup'>
          <ReplayIcon />
        </IconButton>
      )
    }
  ]

  if (error) {
    let errorMessage = 'An error occurred'
    if ('data' in error) {
      const fetchError = error as any
      if (fetchError.data?.detail) {
        errorMessage = String(fetchError.data.detail)
      }
    }
    return <div>Error: {errorMessage}</div>
  }

  return (
    <Box sx={{ height: 600, width: '100%'}}>
        {reloadError && (
            <SnackbarAlert
                open={true}
                onClose={() => setReloadError(null)}
                severity='error'
                message={reloadError}
            />
        )}

      <Typography variant='h4' sx={{ mb: 2, textAlign: 'center' }}>Matchups List</Typography>
      <DataGrid
        rows={matchupsList || []}
        columns={columns}
        loading={isLoading}
        getRowId={(row) => row.id}
        pageSizeOptions={[6, 9, 15, 24]}
        initialState={{
          pagination: {
            paginationModel: { pageSize: 9 }
          }
        }}
        sx={{ '& .MuiDataGrid-cell:hover': { cursor: 'pointer' } }}
      />
    </Box>
  )
}

export default MatchupsListPage
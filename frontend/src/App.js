import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Container, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, Typography, TextField, Button, Box } from '@mui/material';

const API_URL = "http://127.0.0.1:8000/api/get_stats/";  // Corrige l'URL ici

function App() {
    const [stats, setStats] = useState([]);
    const [championCounters, setChampionCounters] = useState(null);
    const [championInput, setChampionInput] = useState('');
    const [error, setError] = useState('');

    // Fonction pour récupérer les stats et les contre du champion
    const fetchStats = (champion) => {
        axios.get(`${API_URL}?champion=${champion}`)
            .then(response => {
                setStats(response.data.stats);
                setChampionCounters(response.data.champion_counters);
                setError('');
            })
            .catch(error => {
                setError("Erreur lors de la récupération des données.");
                console.error("Erreur lors de la récupération des stats :", error);
            });
    };

    useEffect(() => {
        // Charger les stats initiales (sans champion spécifique)
        fetchStats('Azir'); // Remplacer 'Azir' par un champion par défaut si nécessaire
    }, []);

    const handleChampionChange = (event) => {
        setChampionInput(event.target.value);
    };

    const handleFetchStats = () => {
        if (championInput.trim() !== '') {
            fetchStats(championInput);
        } else {
            setError('Veuillez entrer un champion valide.');
        }
    };

    // Fonction pour trier et obtenir les 10 premiers champions basés sur le Winrate
    const getTopCounters = () => {
        if (!championCounters || !championCounters.win_rates) return [];

        const sortedCounters = Object.entries(championCounters.win_rates)
            .sort((a, b) => b[1] - a[1]) // Trier par winrate
            .slice(0, 10); // Prendre les 10 premiers

        return sortedCounters.map(([champion, winRate]) => ({
            champion,
            winRate,
            avgPickDiff: championCounters.avg_pick_diff[champion], // avg_pick_diff = meme nom que dans l'api
            avg_enemy_pick_order: championCounters.avg_pick_order[champion]
        }));
    };

    // Filtrer les stats par rôle
    const filterStatsByRole = (role) => {
        return stats.filter(stat => stat.Role.toLowerCase() === role.toLowerCase());
    };

    return (
        <Container>
            <Typography variant="h4" sx={{ my: 4 }}>Statistiques League of Legends</Typography>

            {/* Champ de saisie pour le champion */}
            <Box sx={{ my: 2 }}>
                <TextField
                    label="Champion"
                    variant="outlined"
                    value={championInput}
                    onChange={handleChampionChange}
                    fullWidth
                />
                <Button
                    variant="contained"
                    color="primary"
                    onClick={handleFetchStats}
                    sx={{ mt: 2 }}
                >
                    Obtenir les stats
                </Button>
            </Box>

            {error && <Typography color="error">{error}</Typography>}

            {/* Affichage des stats de champion pour chaque rôle */}
            {/* Rôle : ADC */}
            <Typography variant="h5" sx={{ my: 2 }}>Rôle : ADC</Typography>
            <TableContainer component={Paper}>
                <Table>
                    <TableHead>
                        <TableRow>
                            <TableCell>Role</TableCell>
                            <TableCell>Champion</TableCell>
                            <TableCell>Games Played</TableCell>
                            <TableCell>Wins</TableCell>
                            <TableCell>Winrate (%)</TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {filterStatsByRole('Adc').map((stat, index) => (
                            <TableRow key={index}>
                                <TableCell>{stat.Role}</TableCell>
                                <TableCell>{stat.Champion}</TableCell>
                                <TableCell>{stat.GamesPlayed}</TableCell>
                                <TableCell>{stat.Wins}</TableCell>
                                <TableCell>{stat.WinratePercentage}</TableCell>
                            </TableRow>
                        ))}
                    </TableBody>
                </Table>
            </TableContainer>

            {/* Rôle : Jung */}
            <Typography variant="h5" sx={{ my: 2 }}>Rôle : Jung</Typography>
            <TableContainer component={Paper}>
                <Table>
                    <TableHead>
                        <TableRow>
                            <TableCell>Role</TableCell>
                            <TableCell>Champion</TableCell>
                            <TableCell>Games Played</TableCell>
                            <TableCell>Wins</TableCell>
                            <TableCell>Winrate (%)</TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {filterStatsByRole('Jun').map((stat, index) => (
                            <TableRow key={index}>
                                <TableCell>{stat.Role}</TableCell>
                                <TableCell>{stat.Champion}</TableCell>
                                <TableCell>{stat.GamesPlayed}</TableCell>
                                <TableCell>{stat.Wins}</TableCell>
                                <TableCell>{stat.WinratePercentage}</TableCell>
                            </TableRow>
                        ))}
                    </TableBody>
                </Table>
            </TableContainer>

            {/* Rôle : Top */}
            <Typography variant="h5" sx={{ my: 2 }}>Rôle : Top</Typography>
            <TableContainer component={Paper}>
                <Table>
                    <TableHead>
                        <TableRow>
                            <TableCell>Role</TableCell>
                            <TableCell>Champion</TableCell>
                            <TableCell>Games Played</TableCell>
                            <TableCell>Wins</TableCell>
                            <TableCell>Winrate (%)</TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {filterStatsByRole('Top').map((stat, index) => (
                            <TableRow key={index}>
                                <TableCell>{stat.Role}</TableCell>
                                <TableCell>{stat.Champion}</TableCell>
                                <TableCell>{stat.GamesPlayed}</TableCell>
                                <TableCell>{stat.Wins}</TableCell>
                                <TableCell>{stat.WinratePercentage}</TableCell>
                            </TableRow>
                        ))}
                    </TableBody>
                </Table>
            </TableContainer>

            {/* Rôle : Mid */}
            <Typography variant="h5" sx={{ my: 2 }}>Rôle : Mid</Typography>
            <TableContainer component={Paper}>
                <Table>
                    <TableHead>
                        <TableRow>
                            <TableCell>Role</TableCell>
                            <TableCell>Champion</TableCell>
                            <TableCell>Games Played</TableCell>
                            <TableCell>Wins</TableCell>
                            <TableCell>Winrate (%)</TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {filterStatsByRole('Mid').map((stat, index) => (
                            <TableRow key={index}>
                                <TableCell>{stat.Role}</TableCell>
                                <TableCell>{stat.Champion}</TableCell>
                                <TableCell>{stat.GamesPlayed}</TableCell>
                                <TableCell>{stat.Wins}</TableCell>
                                <TableCell>{stat.WinratePercentage}</TableCell>
                            </TableRow>
                        ))}
                    </TableBody>
                </Table>
            </TableContainer>

            {/* Rôle : Sup */}
            <Typography variant="h5" sx={{ my: 2 }}>Rôle : Sup</Typography>
            <TableContainer component={Paper}>
                <Table>
                    <TableHead>
                        <TableRow>
                            <TableCell>Role</TableCell>
                            <TableCell>Champion</TableCell>
                            <TableCell>Games Played</TableCell>
                            <TableCell>Wins</TableCell>
                            <TableCell>Winrate (%)</TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {filterStatsByRole('Sup').map((stat, index) => (
                            <TableRow key={index}>
                                <TableCell>{stat.Role}</TableCell>
                                <TableCell>{stat.Champion}</TableCell>
                                <TableCell>{stat.GamesPlayed}</TableCell>
                                <TableCell>{stat.Wins}</TableCell>
                                <TableCell>{stat.WinratePercentage}</TableCell>
                            </TableRow>
                        ))}
                    </TableBody>
                </Table>
            </TableContainer>

            {/* Affichage des 10 meilleurs contre du champion triés par Winrate */}
            {championCounters && (
                <div>
                    <Typography variant="h5" sx={{ my: 4 }}>Top 10 Champion Counters (Basé sur le Winrate)</Typography>
                    <TableContainer component={Paper}>
                        <Table>
                            <TableHead>
                                <TableRow>
                                    <TableCell>Champion</TableCell>
                                    <TableCell>Winrate (%)</TableCell>
                                    <TableCell>Average Pick Diff</TableCell>
                                    <TableCell>Average Pick </TableCell>
                                </TableRow>
                            </TableHead>
                            <TableBody>
                                {getTopCounters().map((counter, index) => (
                                    <TableRow key={index}>
                                        <TableCell>{counter.champion}</TableCell>
                                        <TableCell>{counter.winRate}</TableCell>
                                        <TableCell>{counter.avgPickDiff}</TableCell>
                                        <TableCell>{counter.avg_enemy_pick_order}</TableCell>
                                    </TableRow>
                                ))}
                            </TableBody>
                        </Table>
                    </TableContainer>
                </div>
            )}
        </Container>
    );
}

export default App;

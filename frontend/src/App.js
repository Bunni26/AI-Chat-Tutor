import React from 'react';
import {
  AppBar,
  Toolbar,
  Typography,
} from '@mui/material';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';

import Chat from './components/Chat';

function App() {
  return (
    <Router>
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6" sx={{ flexGrow: 1 }}>
            AI Coding Tutor
          </Typography>
        </Toolbar>
      </AppBar>
      <Routes>
        <Route path="/chat" element={<Chat />} />
        <Route path="/" element={<Navigate to="/chat" replace />} />
      </Routes>
    </Router>
  );
}

export default App;
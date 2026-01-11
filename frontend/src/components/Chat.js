import React, { useState, useRef, useEffect } from 'react';
import {
  Container,
  Box,
  TextField,
  Button,
  Paper,
  Typography,
  CircularProgress,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Alert,
} from '@mui/material';
import { Send as SendIcon } from '@mui/icons-material';
import ReactMarkdown from 'react-markdown';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { vscDarkPlus } from 'react-syntax-highlighter/dist/esm/styles/prism';
import axios from 'axios';

const API_URL = 'http://localhost:5000/api';

function Chat() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [language, setLanguage] = useState('python');
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim()) return;

    const userMessage = input;
    setInput('');
    setLoading(true);
    setError(null);

    const userMessageObj = { type: 'user', content: userMessage };
    setMessages((prev) => [...prev, userMessageObj]);

    try {
      const response = await axios.post(
        `${API_URL}/chat`,
        { message: userMessage, context: messages }
      );

      if (response.data.error) throw new Error(response.data.error);
      if (!response.data.response) throw new Error('Empty response from server');

      const aiMessageObj = { type: 'ai', content: response.data.response };
      setMessages((prev) => [...prev, aiMessageObj]);
    } catch (err) {
      const errorMsg = err.response?.data?.error || err.message || 'Something went wrong';
      setError(errorMsg);
      setMessages((prev) => [...prev, { type: 'error', content: `Error: ${errorMsg}` }]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <Container maxWidth="md" sx={{ height: '100vh', py: 4 }}>
      <Paper elevation={3} sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
        <Box sx={{ p: 2, borderBottom: 1, borderColor: 'divider' }}>
          <Typography variant="h5" component="h1">
            AI Coding Tutor
          </Typography>
          <FormControl size="small" sx={{ mt: 1 }}>
            <InputLabel id="language-select-label">Programming Language</InputLabel>
            <Select
              labelId="language-select-label"
              id="language-select"
              name="language-select"
              value={language}
              label="Programming Language"
              onChange={(e) => setLanguage(e.target.value)}
              inputProps={{
                'aria-label': 'Select programming language',
              }}
            >
              <MenuItem value="python">Python</MenuItem>
              <MenuItem value="javascript">JavaScript</MenuItem>
              <MenuItem value="java">Java</MenuItem>
              <MenuItem value="cpp">C++</MenuItem>
            </Select>
          </FormControl>
          {error && (
            <Alert severity="error" sx={{ mt: 1 }} onClose={() => setError(null)}>
              {error}
            </Alert>
          )}
          {loading && (
            <Alert severity="info" sx={{ mt: 1 }}>
              Processing your request...
            </Alert>
          )}
        </Box>

        <Box sx={{ flex: 1, overflow: 'auto', p: 2, bgcolor: '#f5f5f5' }}>
          {messages.length === 0 ? (
            <Box
              sx={{
                display: 'flex',
                justifyContent: 'center',
                alignItems: 'center',
                height: '100%',
                color: 'text.secondary',
              }}
            >
              <Typography variant="body1">
                Ask me anything about programming! I'm here to help.
              </Typography>
            </Box>
          ) : (
            messages.map((message, index) => (
              <Box
                key={index}
                sx={{
                  mb: 2,
                  display: 'flex',
                  flexDirection: message.type === 'user' ? 'row-reverse' : 'row',
                }}
              >
                <Paper
                  elevation={1}
                  sx={{
                    p: 2,
                    maxWidth: '80%',
                    backgroundColor:
                      message.type === 'user'
                        ? 'primary.light'
                        : message.type === 'error'
                        ? '#ffebee'
                        : '#ffffff',
                    color:
                      message.type === 'user'
                        ? 'primary.contrastText'
                        : message.type === 'error'
                        ? '#c62828'
                        : 'text.primary',
                  }}
                >
                  {message.type === 'user' ? (
                    <Typography>{message.content}</Typography>
                  ) : (
                    <ReactMarkdown
                      components={{
                        code({ node, inline, className, children, ...props }) {
                          const match = /language-(\w+)/.exec(className || '');
                          return !inline && match ? (
                            <SyntaxHighlighter
                              style={vscDarkPlus}
                              language={match[1]}
                              PreTag="div"
                              {...props}
                            >
                              {String(children).replace(/\n$/, '')}
                            </SyntaxHighlighter>
                          ) : (
                            <code {...props} />
                          );
                        },
                      }}
                    >
                      {message.content}
                    </ReactMarkdown>
                  )}
                </Paper>
              </Box>
            ))
          )}
          <div ref={messagesEndRef} />
        </Box>

        <Box sx={{ p: 2, borderTop: 1, borderColor: 'divider' }}>
          <TextField
            fullWidth
            multiline
            maxRows={4}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Type your message here..."
            onKeyPress={handleKeyPress}
            disabled={loading}
            InputProps={{
              endAdornment: (
                <Button
                  variant="contained"
                  color="primary"
                  onClick={handleSend}
                  disabled={loading || !input.trim()}
                  sx={{ ml: 2 }}
                >
                  {loading ? <CircularProgress size={24} /> : <SendIcon />}
                </Button>
              ),
            }}
          />
        </Box>
      </Paper>
    </Container>
  );
}

export default Chat;
import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Send, Bot, Search, PenTool, Sparkles, AlertCircle } from 'lucide-react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { cn } from './lib/utils';

export default function App() {
  const [topic, setTopic] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState('');
  const [error, setError] = useState('');
  const [activeAgent, setActiveAgent] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!topic.trim()) return;

    setIsLoading(true);
    setResult('');
    setError('');
    
    setActiveAgent('Supervisor');
    
    const cycle = setInterval(() => {
      setActiveAgent(prev => {
        if (prev === 'Supervisor') return 'Search';
        if (prev === 'Search') return 'Writer';
        return 'Supervisor';
      });
    }, 4000);

    try {
      const response = await fetch('http://127.0.0.1:8000/api/v1/research', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ topic, depth: 'comprehensive' }),
      });

      if (!response.ok) {
        throw new Error(`Error: ${response.statusText}`);
      }

      const data = await response.json();
      setResult(data.message || 'No report generated.');
    } catch (err: any) {
      setError(err.message || 'An error occurred while communicating with the agents. Is the backend running?');
    } finally {
      clearInterval(cycle);
      setActiveAgent(null);
      setIsLoading(false);
    }
  };

  const agentIcons: Record<string, React.ElementType> = {
    'Supervisor': Bot,
    'Search': Search,
    'Writer': PenTool
  };

  const ActiveIcon = activeAgent ? agentIcons[activeAgent] : null;

  return (
    <div className="relative min-h-screen flex flex-col items-center py-20 px-4">
      {/* Background blobs */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none z-[-1]">
        <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] rounded-full bg-primary/20 blur-[120px] mix-blend-screen animate-blob" />
        <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] rounded-full bg-secondary/20 blur-[120px] mix-blend-screen animate-blob animation-delay-2000" />
      </div>

      <div className="w-full max-w-4xl flex flex-col gap-12">
        {/* Header */}
        <motion.div 
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center space-y-4"
        >
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full glass-panel border-primary/20 text-primary mb-4">
            <Sparkles size={16} />
            <span className="text-sm font-medium tracking-wide uppercase">Multi-Agent System</span>
          </div>
          <h1 className="text-5xl md:text-7xl font-bold tracking-tight">
            Research <span className="text-transparent bg-clip-text bg-gradient-to-r from-primary to-secondary">Anything.</span>
          </h1>
          <p className="text-textMuted text-lg max-w-2xl mx-auto">
            Our autonomous agents will analyze, search, and synthesize a comprehensive report for you in seconds.
          </p>
        </motion.div>

        {/* Input */}
        <motion.form 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          onSubmit={handleSubmit}
          className="relative group"
        >
          <div className="absolute -inset-1 bg-gradient-to-r from-primary to-secondary rounded-2xl blur opacity-25 group-hover:opacity-40 transition duration-1000 group-hover:duration-200" />
          <div className="relative flex items-center glass-panel rounded-2xl p-2">
            <input
              type="text"
              value={topic}
              onChange={(e) => setTopic(e.target.value)}
              placeholder="e.g. Recent advancements in solid state batteries"
              className="w-full bg-transparent border-none text-xl px-6 py-4 text-text placeholder:text-textMuted/50 focus:outline-none focus:ring-0"
              disabled={isLoading}
            />
            <button 
              type="submit" 
              disabled={isLoading || !topic.trim()}
              className="primary-button flex items-center gap-2 ml-2 h-[56px]"
            >
              <span className="font-semibold">{isLoading ? 'Deploying' : 'Start'}</span>
              <Send size={18} className={cn("transition-transform", isLoading && "opacity-0")} />
              {isLoading && (
                <div className="absolute right-6 w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
              )}
            </button>
          </div>
        </motion.form>

        {/* Status / Output */}
        <AnimatePresence mode="wait">
          {isLoading && activeAgent && (
            <motion.div
              key="loading"
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.95 }}
              className="glass-panel p-8 flex flex-col items-center justify-center min-h-[300px] text-center gap-6"
            >
              <div className="relative">
                <div className="absolute inset-0 bg-primary/20 rounded-full blur-xl animate-pulse" />
                <div className="relative bg-surface p-6 rounded-full border border-border shadow-inner">
                  {ActiveIcon && <ActiveIcon size={40} className="text-primary animate-bounce" />}
                </div>
              </div>
              <div className="space-y-2">
                <h3 className="text-2xl font-semibold bg-clip-text text-transparent bg-gradient-to-r from-white to-white/70">
                  {activeAgent} Agent Active
                </h3>
                <p className="text-textMuted">Processing your request through the LangGraph workflow...</p>
              </div>
            </motion.div>
          )}

          {error && (
            <motion.div
              key="error"
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              className="glass-panel p-6 border-red-500/20 bg-red-500/5 flex items-start gap-4 text-red-200"
            >
              <AlertCircle className="shrink-0 mt-1" />
              <div>
                <h3 className="font-semibold text-red-400">Error executing workflow</h3>
                <p className="opacity-80 mt-1">{error}</p>
              </div>
            </motion.div>
          )}

          {result && !isLoading && (
            <motion.div
              key="result"
              initial={{ opacity: 0, y: 40 }}
              animate={{ opacity: 1, y: 0 }}
              className="glass-panel p-8 md:p-12 prose prose-invert max-w-none prose-headings:text-transparent prose-headings:bg-clip-text prose-headings:bg-gradient-to-r prose-headings:from-white prose-headings:to-white/80 prose-a:text-secondary hover:prose-a:text-primary prose-a:transition-colors"
            >
              <ReactMarkdown remarkPlugins={[remarkGfm]}>
                {result}
              </ReactMarkdown>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  );
}

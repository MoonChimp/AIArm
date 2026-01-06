import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { ProgressProvider } from './contexts/ProgressContext';
import Layout from './components/Layout';
import Dashboard from './pages/Dashboard';
import ChatPage from './pages/ChatPage';
import AgentChatPage from './pages/AgentChatPage';
import DeepSitePage from './pages/DeepSitePage';
import ContractBuilderPage from './pages/ContractBuilderPage';
import FluxPage from './pages/FluxPage';
import VideoGenPage from './pages/VideoGenPage';
import MusicPage from './pages/MusicPage';
import FinancePage from './pages/FinancePage';
import AgentsPage from './pages/AgentsPage';
import IntelligencePage from './pages/IntelligencePage';

function App() {
  return (
    <ProgressProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Layout />}>
            <Route index element={<Dashboard />} />
            <Route path="chat" element={<ChatPage />} />
            <Route path="agent/:agentId" element={<AgentChatPage />} />
            <Route path="deepsite" element={<DeepSitePage />} />
            <Route path="nexus-contract-builder" element={<ContractBuilderPage />} />
            <Route path="image-gen" element={<FluxPage />} />
            <Route path="video-gen" element={<VideoGenPage />} />
            <Route path="music" element={<MusicPage />} />
            <Route path="crypto" element={<FinancePage />} />
            <Route path="finance-analytics" element={<AgentChatPage />} />
            <Route path="agents" element={<AgentsPage />} />
            <Route path="intelligence" element={<IntelligencePage />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </ProgressProvider>
  );
}

export default App;

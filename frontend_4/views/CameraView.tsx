import React, { useState } from 'react';
import { api, endpoints } from '../lib/api';
import { UserSession, AIResponse } from '../types';
import { Upload, Play, ShieldAlert, CheckCircle2, Loader2, Info, Camera, Zap, Scan, Hexagon, Cpu, Globe } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

interface CameraViewProps {
  session: UserSession;
}

const CameraView: React.FC<CameraViewProps> = ({ session }) => {
  const [file, setFile] = useState<File | null>(null);
  const [preview, setPreview] = useState<string | null>(null);
  const [analyzing, setAnalyzing] = useState(false);
  const [result, setResult] = useState<{ type: 'success' | 'error' | 'none', msg: string } | null>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const selectedFile = e.target.files[0];
      setFile(selectedFile);
      setPreview(URL.createObjectURL(selectedFile));
      setResult(null);
    }
  };

  const analyzeFrame = async () => {
    if (!file) return;
    setAnalyzing(true);
    setResult(null);
    const formData = new FormData();
    formData.append('image', file, file.name);
    try {
      const aiRes = await api.post<AIResponse>(endpoints.ai.predict, formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      if (aiRes.data.count > 0) {
        const best = aiRes.data.predictions.reduce((prev, current) => (prev.confidence > current.confidence) ? prev : current);
        const reportData = new FormData();
        reportData.append('image', file, file.name);
        reportData.append('type', best.class);
        reportData.append('lat', '23.2599');
        reportData.append('lng', '77.4126');
        reportData.append('address', `${session.displayName} - Autonomous Trigger`);
        const reportRes = await api.post(endpoints.citizen.report, reportData, {
          headers: { 'Content-Type': 'multipart/form-data' }
        });
        setResult({
          type: 'error',
          msg: `ANOMALY DETECTED: ${best.class.toUpperCase()} (${(best.confidence * 100).toFixed(1)}%). TICKET ISSUED: #${reportRes.data.id}.`
        });
      } else {
        setResult({ type: 'success', msg: 'SPATIAL INTEGRITY VERIFIED. NO INFRASTRUCTURE ANOMALIES DETECTED.' });
      }
    } catch (err) {
      console.error(err);
      setResult({ type: 'none', msg: 'ENGINE TIMEOUT: UNABLE TO SYNC WITH BHOPAL NEURAL HUB.' });
    } finally {
      setTimeout(() => setAnalyzing(false), 2500);
    }
  };

  return (
    <div className="max-w-6xl mx-auto space-y-16 pb-20">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-10">
        <motion.div initial={{ opacity: 0, x: -20 }} animate={{ opacity: 1, x: 0 }}>
          <h1 className="text-5xl font-black text-stone-50 tracking-tighter flex items-center gap-4">
            <div className="p-3 bg-amber-600 rounded-2xl shadow-xl shadow-amber-900/30">
              <Camera className="w-10 h-10 text-white" />
            </div> 
            Neural Node
          </h1>
          <p className="text-stone-500 font-bold uppercase tracking-[0.4em] text-[10px] mt-4 ml-2">Active Surveillance Protocol v4.0</p>
        </motion.div>
        
        <div className="flex items-center gap-6 glass-warm px-8 py-5 rounded-[2rem] border border-stone-800 shadow-2xl">
           <div className="flex items-center gap-3">
             <div className="w-2.5 h-2.5 rounded-full bg-emerald-500 animate-pulse shadow-[0_0_10px_rgba(16,185,129,0.5)]"></div>
             <span className="text-[10px] font-black uppercase tracking-[0.2em] text-stone-100">{session.username}</span>
           </div>
           <div className="w-px h-6 bg-stone-800"></div>
           <div className="flex items-center gap-2 text-stone-500">
              <Globe className="w-4 h-4" />
              <span className="text-[10px] font-bold tracking-widest uppercase">23.2599° N, 77.4126° E</span>
           </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-12 items-start">
        {/* Frame Injection Terminal */}
        <div className="lg:col-span-8 space-y-10">
          <motion.div 
            whileHover={{ scale: 1.01 }}
            className="glass-warm p-3 rounded-[4rem] shadow-2xl border border-stone-800 relative group overflow-hidden"
          >
            <div className="absolute top-10 left-10 z-20 flex items-center gap-3 glass-light px-5 py-2.5 rounded-2xl border border-white/10 shadow-xl">
              <div className="w-2 h-2 rounded-full bg-amber-600 animate-pulse"></div>
              <span className="text-[10px] font-black text-white uppercase tracking-[0.3em]">Telemetry Feed</span>
            </div>

            <label className={`relative block w-full h-[550px] rounded-[3.5rem] overflow-hidden transition-all duration-700 cursor-pointer ${!file ? 'bg-stone-900/40 hover:bg-stone-900/60' : ''}`}>
              {preview ? (
                <div className="relative w-full h-full">
                  <img src={preview} alt="Frame" className="w-full h-full object-cover" />
                  {analyzing && <div className="scan-line !bg-gradient-to-r !from-transparent !via-amber-500 !to-transparent !shadow-amber-500/80"></div>}
                  <div className="absolute inset-0 bg-gradient-to-t from-[#0c0a09] via-transparent to-transparent opacity-60"></div>
                  
                  {/* Decorative Neural Grid Overlay */}
                  <div className="absolute inset-0 opacity-10 pointer-events-none bg-[radial-gradient(#fbbf24_1px,transparent_1px)] [background-size:32px_32px]"></div>
                </div>
              ) : (
                <div className="flex flex-col items-center justify-center w-full h-full space-y-8 group/upload">
                  <motion.div 
                    animate={{ y: [0, -10, 0] }}
                    transition={{ duration: 4, repeat: Infinity }}
                    className="w-28 h-28 glass rounded-[2.5rem] flex items-center justify-center text-stone-700 group-hover/upload:bg-amber-600 group-hover/upload:text-white group-hover/upload:border-amber-500 transition-all duration-500 border border-stone-800"
                  >
                    <Upload className="w-10 h-10" />
                  </motion.div>
                  <div className="text-center">
                    <p className="text-stone-300 font-black text-xl tracking-tighter">Inject Neural Frame</p>
                    <p className="text-stone-600 text-[10px] font-black uppercase tracking-[0.4em] mt-3">Ready for spatial analysis</p>
                  </div>
                </div>
              )}
              <input type="file" className="hidden" onChange={handleFileChange} accept="image/*" />
            </label>
          </motion.div>

          <div className="flex gap-6">
            <motion.button
              whileHover={{ scale: 1.02, boxShadow: '0 0 40px rgba(245, 158, 11, 0.2)' }}
              whileTap={{ scale: 0.98 }}
              onClick={analyzeFrame}
              disabled={!file || analyzing}
              className="flex-1 py-7 bg-amber-600 text-white font-black rounded-[2.5rem] shadow-2xl shadow-amber-900/40 hover:bg-amber-500 disabled:opacity-30 disabled:shadow-none transition-all flex items-center justify-center gap-4 uppercase tracking-[0.3em] text-[10px]"
            >
              {analyzing ? (
                <>
                  <Loader2 className="w-6 h-6 animate-spin" />
                  Computing Neural Mesh...
                </>
              ) : (
                <>
                  <Zap className="w-6 h-6" />
                  Initiate Spatial Scan
                </>
              )}
            </motion.button>
            
            <button
              onClick={() => { setFile(null); setPreview(null); setResult(null); }}
              className="px-10 py-7 glass-warm text-stone-500 border border-stone-800 font-black rounded-[2.5rem] hover:text-stone-300 transition-all uppercase tracking-[0.3em] text-[10px]"
            >
              Flush Node
            </button>
          </div>
        </div>

        {/* Diagnostic Output */}
        <div className="lg:col-span-4 space-y-10">
           <motion.div 
             initial={{ opacity: 0, x: 20 }}
             animate={{ opacity: 1, x: 0 }}
             className="glass-card p-10 rounded-[3.5rem] border border-stone-800 shadow-2xl h-full flex flex-col"
           >
              <h2 className="text-2xl font-black text-stone-50 mb-10 flex items-center gap-4 tracking-tighter">
                <div className="p-3 glass rounded-xl border border-white/5">
                  <Cpu className="w-6 h-6 text-amber-500" />
                </div> 
                Diagnostic Hub
              </h2>

              <div className="space-y-8 flex-1">
                {!result && !analyzing && (
                  <div className="flex flex-col items-center justify-center py-24 text-center space-y-8 opacity-30 group">
                    <Hexagon className="w-24 h-24 text-stone-700 animate-float-soft" />
                    <p className="text-stone-600 font-black uppercase tracking-[0.4em] text-[10px]">Awaiting Data Injection</p>
                  </div>
                )}

                <AnimatePresence>
                  {analyzing && (
                    <motion.div 
                      initial={{ opacity: 0 }}
                      animate={{ opacity: 1 }}
                      exit={{ opacity: 0 }}
                      className="space-y-8"
                    >
                       {[1,2,3,4].map(i => (
                         <div key={i} className="h-16 glass-light rounded-2xl border border-white/5 flex items-center px-6">
                           <div className="w-4 h-4 bg-amber-500/20 rounded-full mr-4 border border-amber-500/40"></div>
                           <div className="h-2 flex-1 bg-stone-800 rounded-full overflow-hidden">
                              <motion.div 
                                initial={{ x: '-100%' }}
                                animate={{ x: '100%' }}
                                transition={{ duration: 1.5, repeat: Infinity, ease: 'linear', delay: i * 0.2 }}
                                className="w-full h-full bg-amber-500/40"
                              />
                           </div>
                         </div>
                       ))}
                       <p className="text-center text-[10px] font-black text-amber-500 uppercase tracking-[0.5em] mt-12 animate-pulse">Running Neural Inference...</p>
                    </motion.div>
                  )}
                </AnimatePresence>

                {result && !analyzing && (
                  <motion.div 
                    initial={{ scale: 0.95, opacity: 0 }}
                    animate={{ scale: 1, opacity: 1 }}
                    className={`p-10 rounded-[3rem] border ${result.type === 'error' ? 'bg-orange-500/5 border-orange-500/20 text-orange-200' : 'bg-emerald-500/5 border-emerald-500/20 text-emerald-200'} shadow-2xl amber-glow`}
                  >
                    <div className="flex flex-col items-center text-center space-y-8">
                      <div className={`w-24 h-24 rounded-[2.5rem] flex items-center justify-center ${result.type === 'error' ? 'bg-orange-500 text-white shadow-2xl shadow-orange-900/50' : 'bg-emerald-500 text-white shadow-2xl shadow-emerald-900/50'}`}>
                        {result.type === 'error' ? <ShieldAlert className="w-12 h-12" /> : <CheckCircle2 className="w-12 h-12" />}
                      </div>
                      <div className="space-y-4">
                        <h4 className="font-black text-3xl tracking-tighter leading-none text-white">
                          {result.type === 'error' ? 'Detection Conflict' : 'Clear Sweep'}
                        </h4>
                        <p className="text-xs font-bold opacity-70 leading-relaxed uppercase tracking-[0.1em]">
                          {result.msg}
                        </p>
                      </div>
                      <div className="pt-8 w-full border-t border-white/5 flex justify-between items-center text-[9px] font-black uppercase tracking-[0.4em] opacity-40">
                        <span>Confidence: 94.2%</span>
                        <span>v4.20-Engine</span>
                      </div>
                    </div>
                  </motion.div>
                )}
              </div>

              <div className="mt-12 p-8 glass-warm rounded-[2.5rem] border border-stone-800/50 space-y-8">
                 <h4 className="text-[10px] font-black text-stone-600 uppercase tracking-[0.4em]">Node Diagnostics</h4>
                 <div className="space-y-5">
                    <div className="flex justify-between items-center">
                      <span className="text-[10px] font-bold text-stone-500 uppercase tracking-widest">Signal State</span>
                      <span className="text-[10px] font-black text-emerald-500 uppercase tracking-widest">Master Synchronized</span>
                    </div>
                    <div className="flex justify-between items-center">
                      <span className="text-[10px] font-bold text-stone-500 uppercase tracking-widest">Latency</span>
                      <span className="text-[10px] font-black text-amber-500 uppercase tracking-widest">12ms Hub-Sync</span>
                    </div>
                 </div>
              </div>
           </motion.div>
        </div>
      </div>
    </div>
  );
};

export default CameraView;